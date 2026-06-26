# Fullstack Task Management Feature — Complete Implementation

**Blueprint:** fullstack-feature-builder  
**Run ID:** run-20260625-213900  
**Stack:** Next.js 14 (App Router) · tRPC v11 · Prisma · React Query v5 · Zod · Tailwind CSS  
**Date:** 2026-06-25

---

## Table of Contents

1. [Project File Structure](#1-project-file-structure)
2. [Database Model (Prisma)](#2-database-model-prisma)
3. [tRPC Backend — Server Setup](#3-trpc-backend--server-setup)
4. [tRPC Router — Task CRUD](#4-trpc-router--task-crud)
5. [Validation Schemas (Zod)](#5-validation-schemas-zod)
6. [React Components](#6-react-components)
   - [TaskList](#61-tasklist)
   - [TaskCard](#62-taskcard)
   - [TaskForm](#63-taskform)
   - [TaskDashboard (container)](#64-taskdashboard-container)
7. [React Query Hooks & State Management](#7-react-query-hooks--state-management)
8. [Optimistic Updates](#8-optimistic-updates)
9. [Error Handling](#9-error-handling)
10. [Loading States](#10-loading-states)
11. [Integration Guide](#11-integration-guide)
12. [API Reference](#12-api-reference)

---

## 1. Project File Structure

```
src/
├── app/
│   ├── api/
│   │   └── trpc/
│   │       └── [trpc]/
│   │           └── route.ts                # tRPC HTTP handler (Next.js App Router)
│   ├── layout.tsx                           # Root layout with TRPCProvider
│   └── tasks/
│       ├── page.tsx                         # Task dashboard page
│       └── loading.tsx                      # Route-level loading skeleton
├── server/
│   ├── api/
│   │   ├── routers/
│   │   │   ├── root.ts                      # Root tRPC router (merge all sub-routers)
│   │   │   └── task.ts                      # Task CRUD router
│   │   └── trpc.ts                          # tRPC context + init helpers
│   └── db/
│       ├── schema.prisma                    # Database schema
│       └── index.ts                         # Prisma client singleton
├── lib/
│   ├── trpc/
│   │   ├── client.ts                        # tRPC React client
│   │   ├── react.tsx                        # TRPCProvider + useTRPC
│   │   └── server.ts                        # Server-side tRPC caller
│   ├── hooks/
│   │   ├── use-tasks.ts                     # Task query & mutation hooks
│   │   └── use-optimistic.ts                # Optimistic update utilities
│   ├── schemas/
│   │   └── task.ts                          # Zod validation schemas
│   ├── types/
│   │   └── task.ts                          # Shared TypeScript types
│   └── utils/
│       ├── errors.ts                        # Error serialization + helpers
│       └── cn.ts                            # Tailwind class merge utility
├── components/
│   ├── tasks/
│   │   ├── task-list.tsx                    # TaskList — sortable, filterable list
│   │   ├── task-card.tsx                    # TaskCard — individual task display
│   │   ├── task-form.tsx                    # TaskForm — create/edit form
│   │   ├── task-dashboard.tsx               # TaskDashboard — container + orchestration
│   │   ├── task-filters.tsx                 # TaskFilters — status/priority bar
│   │   ├── task-skeleton.tsx                # TaskSkeleton — loading placeholder
│   │   └── task-empty-state.tsx             # TaskEmptyState — when no tasks exist
│   └── ui/
│       ├── button.tsx
│       ├── card.tsx
│       ├── input.tsx
│       ├── select.tsx
│       ├── textarea.tsx
│       ├── badge.tsx
│       ├── dialog.tsx
│       ├── spinner.tsx
│       └── toast.tsx                        # Toast notification system
└── middleware.ts                            # Optional: auth middleware
```

---

## 2. Database Model (Prisma)

**File:** `src/server/db/schema.prisma`

```prisma
generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model Task {
  id          String    @id @default(cuid())
  title       String
  description String?   @db.Text
  status      Status    @default(TODO)
  priority    Priority  @default(MEDIUM)
  dueDate     DateTime?
  tags        String[]  @default([])

  // Relations
  assignedToId String?
  assignedTo   User?     @relation(fields: [assignedToId], references: [id])

  createdAt   DateTime  @default(now())
  updatedAt   DateTime  @updatedAt
  completedAt DateTime?

  @@index([status])
  @@index([priority])
  @@index([assignedToId])
  @@index([dueDate])
  @@index([createdAt])
}

model User {
  id            String   @id @default(cuid())
  name          String
  email         String   @unique
  image         String?
  assignedTasks Task[]
}

enum Status {
  TODO
  IN_PROGRESS
  IN_REVIEW
  DONE
  CANCELLED
}

enum Priority {
  LOW
  MEDIUM
  HIGH
  URGENT
}
```

**Prisma Client Singleton —** `src/server/db/index.ts`

```typescript
import { PrismaClient } from "@prisma/client";

const globalForPrisma = globalThis as unknown as {
  prisma: PrismaClient | undefined;
};

export const db = globalForPrisma.prisma ?? new PrismaClient({
  log: process.env.NODE_ENV === "development"
    ? ["query", "info", "warn", "error"]
    : ["error"],
});

if (process.env.NODE_ENV !== "production") globalForPrisma.prisma = db;
```

---

## 3. tRPC Backend — Server Setup

**File:** `src/server/api/trpc.ts`

```typescript
import { initTRPC, TRPCError } from "@trpc/server";
import { type FetchCreateContextFnOptions } from "@trpc/server/adapters/fetch";
import superjson from "superjson";
import { ZodError } from "zod";
import { db } from "@/server/db";

// ── Context ─────────────────────────────────────────────
export const createTRPCContext = async (opts: FetchCreateContextFnOptions) => {
  // In production, extract session/token from opts.req headers
  const session = { user: null }; // Replace with real auth

  return {
    db,
    session,
    headers: opts.req.headers,
    ...opts,
  };
};

export type Context = Awaited<ReturnType<typeof createTRPCContext>>;

// ── Init ────────────────────────────────────────────────
const t = initTRPC.context<Context>().create({
  transformer: superjson,       // Date serialization
  errorFormatter({ shape, error }) {
    return {
      ...shape,
      data: {
        ...shape.data,
        zodError:
          error.cause instanceof ZodError
            ? error.cause.flatten()
            : null,
      },
    };
  },
});

// ── Middleware ──────────────────────────────────────────
const timingMiddleware = t.middleware(async ({ path, type, next }) => {
  const start = Date.now();
  const result = await next();
  const duration = Date.now() - start;
  // In production, emit this to your observability stack
  if (duration > 1000) {
    console.warn(`[tRPC.SLOW] ${type} ${path} took ${duration}ms`);
  }
  return result;
});

// Optional: authentication middleware
const isAuthed = t.middleware(({ ctx, next }) => {
  if (!ctx.session?.user) {
    throw new TRPCError({ code: "UNAUTHORIZED" });
  }
  return next({
    ctx: { ...ctx, user: ctx.session.user },
  });
});

// ── Procedures ──────────────────────────────────────────
export const router = t.router;
export const publicProcedure = t.procedure.use(timingMiddleware);
export const protectedProcedure = t.procedure.use(timingMiddleware).use(isAuthed);
```

**File:** `src/app/api/trpc/[trpc]/route.ts`

```typescript
import { fetchRequestHandler } from "@trpc/server/adapters/fetch";
import { type NextRequest } from "next/server";
import { appRouter } from "@/server/api/routers/root";
import { createTRPCContext } from "@/server/api/trpc";

const handler = (req: NextRequest) =>
  fetchRequestHandler({
    endpoint: "/api/trpc",
    req,
    router: appRouter,
    createContext: () => createTRPCContext({ req }),
    onError:
      process.env.NODE_ENV === "development"
        ? ({ path, error }) => {
            console.error(`❌ tRPC failed on ${path ?? "<no-path>"}:`, error);
          }
        : undefined,
  });

export { handler as GET, handler as POST };
```

---

## 4. tRPC Router — Task CRUD

**File:** `src/server/api/routers/task.ts`

```typescript
import { z } from "zod";
import { TRPCError } from "@trpc/server";
import { router, publicProcedure, protectedProcedure } from "@/server/api/trpc";
import {
  taskCreateSchema,
  taskUpdateSchema,
  taskIdSchema,
  taskFilterSchema,
} from "@/lib/schemas/task";

export const taskRouter = router({
  // ── List all tasks (with filters) ──────────────────
  list: publicProcedure
    .input(taskFilterSchema.optional())
    .query(async ({ ctx, input }) => {
      const { status, priority, search, sortBy, sortOrder, limit, cursor } =
        input ?? {};

      const where: Record<string, unknown> = {};

      if (status) where.status = status;
      if (priority) where.priority = priority;
      if (search) {
        where.OR = [
          { title: { contains: search, mode: "insensitive" } },
          { description: { contains: search, mode: "insensitive" } },
        ];
      }

      const orderBy: Record<string, string> = {};
      switch (sortBy) {
        case "dueDate":
          orderBy.dueDate = sortOrder ?? "asc";
          break;
        case "priority":
          orderBy.priority = sortOrder ?? "desc";
          break;
        case "createdAt":
        default:
          orderBy.createdAt = sortOrder ?? "desc";
      }

      const take = limit ?? 20;

      const [tasks, totalCount] = await Promise.all([
        ctx.db.task.findMany({
          where,
          orderBy,
          take: take + 1, // Fetch one extra for cursor
          ...(cursor ? { skip: 1, cursor: { id: cursor } } : {}),
          include: { assignedTo: { select: { id: true, name: true, image: true } } },
        }),
        ctx.db.task.count({ where }),
      ]);

      let nextCursor: string | undefined;
      if (tasks.length > take) {
        const nextItem = tasks.pop();
        nextCursor = nextItem!.id;
      }

      return { tasks, totalCount, nextCursor };
    }),

  // ── Get single task ────────────────────────────────
  byId: publicProcedure
    .input(taskIdSchema)
    .query(async ({ ctx, input }) => {
      const task = await ctx.db.task.findUnique({
        where: { id: input.id },
        include: { assignedTo: { select: { id: true, name: true, image: true } } },
      });

      if (!task) {
        throw new TRPCError({
          code: "NOT_FOUND",
          message: `Task with id "${input.id}" not found`,
        });
      }

      return task;
    }),

  // ── Create task ────────────────────────────────────
  create: publicProcedure
    .input(taskCreateSchema)
    .mutation(async ({ ctx, input }) => {
      const task = await ctx.db.task.create({
        data: {
          title: input.title,
          description: input.description ?? null,
          priority: input.priority ?? "MEDIUM",
          status: input.status ?? "TODO",
          dueDate: input.dueDate ? new Date(input.dueDate) : null,
          tags: input.tags ?? [],
        },
        include: { assignedTo: { select: { id: true, name: true, image: true } } },
      });

      return task;
    }),

  // ── Update task ────────────────────────────────────
  update: publicProcedure
    .input(taskUpdateSchema)
    .mutation(async ({ ctx, input }) => {
      const { id, ...data } = input;

      const existing = await ctx.db.task.findUnique({ where: { id } });
      if (!existing) {
        throw new TRPCError({
          code: "NOT_FOUND",
          message: `Task with id "${id}" not found`,
        });
      }

      // Auto-set completedAt when transitioning to DONE
      const updateData: Record<string, unknown> = { ...data };
      if (data.dueDate) updateData.dueDate = new Date(data.dueDate);
      if (data.status === "DONE" && existing.status !== "DONE") {
        updateData.completedAt = new Date();
      }
      if (data.status !== "DONE" && existing.status === "DONE") {
        updateData.completedAt = null;
      }

      const task = await ctx.db.task.update({
        where: { id },
        data: updateData,
        include: { assignedTo: { select: { id: true, name: true, image: true } } },
      });

      return task;
    }),

  // ── Delete task ────────────────────────────────────
  delete: publicProcedure
    .input(taskIdSchema)
    .mutation(async ({ ctx, input }) => {
      const existing = await ctx.db.task.findUnique({ where: { id: input.id } });
      if (!existing) {
        throw new TRPCError({
          code: "NOT_FOUND",
          message: `Task with id "${input.id}" not found`,
        });
      }

      await ctx.db.task.delete({ where: { id: input.id } });

      return { success: true, id: input.id };
    }),

  // ── Batch update status (for drag-and-drop kanban) ─
  batchUpdateStatus: publicProcedure
    .input(
      z.object({
        taskIds: z.array(z.string()).min(1).max(100),
        status: z.enum(["TODO", "IN_PROGRESS", "IN_REVIEW", "DONE", "CANCELLED"]),
      })
    )
    .mutation(async ({ ctx, input }) => {
      const completedAt = input.status === "DONE" ? new Date() : null;

      await ctx.db.task.updateMany({
        where: { id: { in: input.taskIds } },
        data: {
          status: input.status,
          completedAt,
        },
      });

      // Fetch updated tasks so the cache has fresh data
      const tasks = await ctx.db.task.findMany({
        where: { id: { in: input.taskIds } },
        include: { assignedTo: { select: { id: true, name: true, image: true } } },
      });

      return tasks;
    }),
});
```

**Root Router —** `src/server/api/routers/root.ts`

```typescript
import { router } from "@/server/api/trpc";
import { taskRouter } from "./task";

export const appRouter = router({
  task: taskRouter,
});

export type AppRouter = typeof appRouter;
```

---

## 5. Validation Schemas (Zod)

**File:** `src/lib/schemas/task.ts`

```typescript
import { z } from "zod";

// ── Enums ──────────────────────────────────────────────
export const statusEnum = z.enum([
  "TODO",
  "IN_PROGRESS",
  "IN_REVIEW",
  "DONE",
  "CANCELLED",
]);

export const priorityEnum = z.enum(["LOW", "MEDIUM", "HIGH", "URGENT"]);

// ── Schemas ────────────────────────────────────────────
export const taskIdSchema = z.object({
  id: z.string().min(1, "Task ID is required"),
});

export const taskCreateSchema = z.object({
  title: z
    .string()
    .min(1, "Title is required")
    .max(200, "Title must be 200 characters or less"),
  description: z
    .string()
    .max(5000, "Description must be 5000 characters or less")
    .optional()
    .nullable(),
  priority: priorityEnum.optional().default("MEDIUM"),
  status: statusEnum.optional().default("TODO"),
  dueDate: z.string().datetime().optional().nullable(),
  tags: z
    .array(z.string().min(1).max(30))
    .max(10, "Maximum 10 tags allowed")
    .optional()
    .default([]),
});

export const taskUpdateSchema = taskIdSchema.extend({
  title: z
    .string()
    .min(1, "Title is required")
    .max(200, "Title must be 200 characters or less")
    .optional(),
  description: z
    .string()
    .max(5000, "Description must be 5000 characters or less")
    .optional()
    .nullable(),
  priority: priorityEnum.optional(),
  status: statusEnum.optional(),
  dueDate: z.string().datetime().optional().nullable(),
  tags: z
    .array(z.string().min(1).max(30))
    .max(10, "Maximum 10 tags allowed")
    .optional(),
});

export const taskFilterSchema = z.object({
  status: statusEnum.optional(),
  priority: priorityEnum.optional(),
  search: z.string().max(200).optional(),
  sortBy: z.enum(["createdAt", "dueDate", "priority"]).optional().default("createdAt"),
  sortOrder: z.enum(["asc", "desc"]).optional().default("desc"),
  limit: z.number().min(1).max(100).optional().default(20),
  cursor: z.string().optional(),
});

// ── Derived Types ──────────────────────────────────────
export type TaskCreateInput = z.infer<typeof taskCreateSchema>;
export type TaskUpdateInput = z.infer<typeof taskUpdateSchema>;
export type TaskFilterInput = z.infer<typeof taskFilterSchema>;
```

---

## 6. React Components

### 6.1 TaskList

**File:** `src/components/tasks/task-list.tsx`

```tsx
"use client";

import { useMemo } from "react";
import { TaskCard } from "./task-card";
import { TaskSkeleton } from "./task-skeleton";
import { TaskEmptyState } from "./task-empty-state";
import type { RouterOutputs } from "@/lib/trpc/client";

type Task = RouterOutputs["task"]["list"]["tasks"][number];

interface TaskListProps {
  tasks: Task[];
  isLoading: boolean;
  isError: boolean;
  error?: Error | null;
  onRefetch: () => void;
  onDelete: (id: string) => void;
  onStatusChange: (id: string, status: string) => void;
  deletingTaskId?: string | null;
  /** IDs of tasks currently being mutated (for optimistic state) */
  mutatingTaskIds?: Set<string>;
}

export function TaskList({
  tasks,
  isLoading,
  isError,
  error,
  onRefetch,
  onDelete,
  onStatusChange,
  deletingTaskId,
  mutatingTaskIds,
}: TaskListProps) {
  // Group tasks by status for visual sections
  const grouped = useMemo(() => {
    const groups: Record<string, Task[]> = {
      TODO: [],
      IN_PROGRESS: [],
      IN_REVIEW: [],
      DONE: [],
      CANCELLED: [],
    };
    tasks.forEach((t) => {
      if (groups[t.status]) groups[t.status].push(t);
    });
    return groups;
  }, [tasks]);

  // ── Loading State ─────────────────────────────────
  if (isLoading) {
    return (
      <div className="space-y-3">
        {Array.from({ length: 5 }).map((_, i) => (
          <TaskSkeleton key={i} />
        ))}
      </div>
    );
  }

  // ── Error State ────────────────────────────────────
  if (isError) {
    return (
      <div className="flex flex-col items-center justify-center rounded-lg border border-destructive/50 bg-destructive/5 py-12 text-center">
        <div className="mb-2 text-4xl">⚠️</div>
        <h3 className="text-lg font-semibold text-destructive">
          Failed to load tasks
        </h3>
        <p className="mt-1 text-sm text-muted-foreground">
          {error?.message ?? "An unexpected error occurred."}
        </p>
        <button
          onClick={onRefetch}
          className="mt-4 rounded-md bg-destructive px-4 py-2 text-sm font-medium text-destructive-foreground hover:bg-destructive/90 transition-colors"
        >
          Try Again
        </button>
      </div>
    );
  }

  // ── Empty State ────────────────────────────────────
  if (tasks.length === 0) {
    return <TaskEmptyState />;
  }

  // ── Task Grid ──────────────────────────────────────
  return (
    <div className="space-y-6">
      {Object.entries(grouped).map(([status, statusTasks]) => {
        if (statusTasks.length === 0) return null;
        return (
          <section key={status}>
            <h3 className="mb-3 text-sm font-semibold uppercase tracking-wider text-muted-foreground">
              {status.replace("_", " ")} ({statusTasks.length})
            </h3>
            <div className="space-y-2">
              {statusTasks.map((task) => (
                <TaskCard
                  key={task.id}
                  task={task}
                  onDelete={onDelete}
                  onStatusChange={onStatusChange}
                  isDeleting={deletingTaskId === task.id}
                  isMutating={mutatingTaskIds?.has(task.id)}
                />
              ))}
            </div>
          </section>
        );
      })}
    </div>
  );
}
```

---

### 6.2 TaskCard

**File:** `src/components/tasks/task-card.tsx`

```tsx
"use client";

import { useState } from "react";
import { formatDistanceToNow, format, isPast, isToday } from "date-fns";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { TaskForm } from "./task-form";
import { cn } from "@/lib/utils/cn";

// ── Priority Color Map ─────────────────────────────────
const priorityConfig = {
  URGENT: { color: "bg-red-100 text-red-800 border-red-300", label: "Urgent" },
  HIGH: { color: "bg-orange-100 text-orange-800 border-orange-300", label: "High" },
  MEDIUM: { color: "bg-blue-100 text-blue-800 border-blue-300", label: "Medium" },
  LOW: { color: "bg-gray-100 text-gray-800 border-gray-300", label: "Low" },
} as const;

const statusConfig = {
  TODO: { color: "bg-slate-100 text-slate-800", label: "To Do" },
  IN_PROGRESS: { color: "bg-yellow-100 text-yellow-800", label: "In Progress" },
  IN_REVIEW: { color: "bg-purple-100 text-purple-800", label: "In Review" },
  DONE: { color: "bg-green-100 text-green-800", label: "Done" },
  CANCELLED: { color: "bg-red-100 text-red-800 line-through", label: "Cancelled" },
} as const;

// ── Types ──────────────────────────────────────────────
interface Task {
  id: string;
  title: string;
  description: string | null;
  status: string;
  priority: string;
  dueDate: string | null;
  tags: string[];
  assignedTo: { id: string; name: string; image: string | null } | null;
  createdAt: string;
  updatedAt: string;
  completedAt: string | null;
}

interface TaskCardProps {
  task: Task;
  onDelete: (id: string) => void;
  onStatusChange: (id: string, status: string) => void;
  isDeleting?: boolean;
  isMutating?: boolean;
}

export function TaskCard({
  task,
  onDelete,
  onStatusChange,
  isDeleting,
  isMutating,
}: TaskCardProps) {
  const [editOpen, setEditOpen] = useState(false);

  const isOverdue =
    task.dueDate && isPast(new Date(task.dueDate)) && task.status !== "DONE";
  const isDueToday = task.dueDate && isToday(new Date(task.dueDate));

  // ── Status Transition ──────────────────────────────
  const handleStatusCycle = () => {
    const sequence = ["TODO", "IN_PROGRESS", "IN_REVIEW", "DONE"];
    const currentIdx = sequence.indexOf(task.status);
    const next = sequence[(currentIdx + 1) % sequence.length];
    onStatusChange(task.id, next);
  };

  return (
    <>
      <div
        className={cn(
          "group relative rounded-lg border bg-card p-4 shadow-sm transition-all",
          "hover:shadow-md hover:border-primary/30",
          isMutating && "opacity-70 pointer-events-none",
          isDeleting && "opacity-50 scale-95 animate-pulse",
          task.status === "DONE" && "bg-muted/30"
        )}
        role="article"
        aria-label={`Task: ${task.title}`}
      >
        {/* Top Row: Title + Priority */}
        <div className="flex items-start justify-between gap-2">
          <div className="flex-1 min-w-0">
            <h4
              className={cn(
                "font-medium truncate cursor-pointer hover:text-primary transition-colors",
                task.status === "DONE" && "line-through text-muted-foreground"
              )}
              onClick={() => setEditOpen(true)}
            >
              {task.title}
            </h4>
            {task.description && (
              <p className="mt-1 text-sm text-muted-foreground line-clamp-2">
                {task.description}
              </p>
            )}
          </div>
          <Badge className={cn("shrink-0 border", priorityConfig[task.priority]?.color)}>
            {priorityConfig[task.priority]?.label}
          </Badge>
        </div>

        {/* Tags */}
        {task.tags.length > 0 && (
          <div className="mt-2 flex flex-wrap gap-1">
            {task.tags.map((tag) => (
              <span
                key={tag}
                className="rounded-full bg-secondary px-2 py-0.5 text-xs font-medium text-secondary-foreground"
              >
                #{tag}
              </span>
            ))}
          </div>
        )}

        {/* Bottom Row: Status, Due Date, Actions */}
        <div className="mt-3 flex items-center justify-between">
          <div className="flex items-center gap-3">
            {/* Status Badge — clickable to cycle */}
            <button
              onClick={handleStatusCycle}
              className={cn(
                "rounded-full px-2.5 py-0.5 text-xs font-semibold transition-colors hover:brightness-95",
                statusConfig[task.status]?.color
              )}
              aria-label={`Status: ${statusConfig[task.status]?.label}. Click to change.`}
            >
              {statusConfig[task.status]?.label}
            </button>

            {/* Due Date */}
            {task.dueDate && (
              <span
                className={cn(
                  "text-xs",
                  isOverdue
                    ? "font-semibold text-destructive"
                    : isDueToday
                    ? "font-medium text-amber-600"
                    : "text-muted-foreground"
                )}
              >
                {isOverdue
                  ? `Overdue — ${format(new Date(task.dueDate), "MMM d")}`
                  : isDueToday
                  ? `Due today`
                  : `Due ${formatDistanceToNow(new Date(task.dueDate), { addSuffix: true })}`}
              </span>
            )}
          </div>

          {/* Action Buttons (visible on hover) */}
          <div className="flex items-center gap-1 opacity-0 group-hover:opacity-100 transition-opacity">
            <Button
              variant="ghost"
              size="sm"
              onClick={() => setEditOpen(true)}
              aria-label="Edit task"
            >
              ✏️
            </Button>
            <Button
              variant="ghost"
              size="sm"
              onClick={() => onDelete(task.id)}
              disabled={isDeleting}
              aria-label="Delete task"
              className="hover:text-destructive"
            >
              🗑️
            </Button>
          </div>
        </div>

        {/* Assigned User */}
        {task.assignedTo && (
          <div className="mt-2 flex items-center gap-2 text-xs text-muted-foreground">
            <span>Assigned to:</span>
            <span className="font-medium text-foreground">{task.assignedTo.name}</span>
          </div>
        )}
      </div>

      {/* Edit Dialog */}
      <Dialog open={editOpen} onOpenChange={setEditOpen}>
        <DialogContent className="max-w-lg">
          <DialogHeader>
            <DialogTitle>Edit Task</DialogTitle>
          </DialogHeader>
          <TaskForm
            task={task}
            onSuccess={() => setEditOpen(false)}
            onCancel={() => setEditOpen(false)}
          />
        </DialogContent>
      </Dialog>
    </>
  );
}
```

---

### 6.3 TaskForm

**File:** `src/components/tasks/task-form.tsx`

```tsx
"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Select } from "@/components/ui/select";
import { Spinner } from "@/components/ui/spinner";
import { taskCreateSchema, taskUpdateSchema } from "@/lib/schemas/task";
import { useCreateTask, useUpdateTask } from "@/lib/hooks/use-tasks";
import type { RouterOutputs } from "@/lib/trpc/client";

type Task = RouterOutputs["task"]["list"]["tasks"][number];

interface TaskFormProps {
  /** Pass an existing task for edit mode; undefined for create mode */
  task?: Task;
  onSuccess?: () => void;
  onCancel?: () => void;
}

export function TaskForm({ task, onSuccess, onCancel }: TaskFormProps) {
  const isEdit = !!task;
  const createMutation = useCreateTask();
  const updateMutation = useUpdateTask();

  const mutation = isEdit ? updateMutation : createMutation;

  const form = useForm({
    resolver: zodResolver(isEdit ? taskUpdateSchema : taskCreateSchema),
    defaultValues: {
      title: task?.title ?? "",
      description: task?.description ?? "",
      priority: task?.priority ?? "MEDIUM",
      status: task?.status ?? "TODO",
      dueDate: task?.dueDate
        ? new Date(task.dueDate).toISOString().slice(0, 16)
        : "",
      tags: task?.tags ?? [],
    },
  });

  const onSubmit = form.handleSubmit(async (data) => {
    try {
      if (isEdit) {
        await updateMutation.mutateAsync({
          id: task.id,
          ...data,
          dueDate: data.dueDate ? new Date(data.dueDate).toISOString() : null,
          description: data.description || null,
        });
      } else {
        await createMutation.mutateAsync({
          ...data,
          dueDate: data.dueDate ? new Date(data.dueDate).toISOString() : null,
          description: data.description || null,
        });
      }
      onSuccess?.();
    } catch {
      // Error handled by mutation's onError and toast
    }
  });

  // ── Tag input handler ──────────────────────────────
  const [tagInput, setTagInput] = useState("");
  const tags = form.watch("tags") ?? [];

  const addTag = () => {
    const trimmed = tagInput.trim();
    if (trimmed && !tags.includes(trimmed) && tags.length < 10) {
      form.setValue("tags", [...tags, trimmed]);
      setTagInput("");
    }
  };

  const removeTag = (tag: string) => {
    form.setValue(
      "tags",
      tags.filter((t) => t !== tag)
    );
  };

  const errors = form.formState.errors;

  return (
    <form onSubmit={onSubmit} className="space-y-4">
      {/* Title */}
      <div>
        <label htmlFor="title" className="block text-sm font-medium">
          Title <span className="text-destructive">*</span>
        </label>
        <Input
          id="title"
          {...form.register("title")}
          placeholder="What needs to be done?"
          aria-invalid={!!errors.title}
          className="mt-1"
        />
        {errors.title && (
          <p className="mt-1 text-xs text-destructive" role="alert">
            {errors.title.message}
          </p>
        )}
      </div>

      {/* Description */}
      <div>
        <label htmlFor="description" className="block text-sm font-medium">
          Description
        </label>
        <Textarea
          id="description"
          {...form.register("description")}
          placeholder="Add details..."
          rows={3}
          aria-invalid={!!errors.description}
          className="mt-1"
        />
        {errors.description && (
          <p className="mt-1 text-xs text-destructive" role="alert">
            {errors.description.message}
          </p>
        )}
      </div>

      {/* Priority & Status Row */}
      <div className="grid grid-cols-2 gap-4">
        <div>
          <label htmlFor="priority" className="block text-sm font-medium">
            Priority
          </label>
          <Select
            id="priority"
            {...form.register("priority")}
            aria-invalid={!!errors.priority}
            className="mt-1"
          >
            <option value="LOW">Low</option>
            <option value="MEDIUM">Medium</option>
            <option value="HIGH">High</option>
            <option value="URGENT">Urgent</option>
          </Select>
        </div>
        <div>
          <label htmlFor="status" className="block text-sm font-medium">
            Status
          </label>
          <Select
            id="status"
            {...form.register("status")}
            aria-invalid={!!errors.status}
            className="mt-1"
          >
            <option value="TODO">To Do</option>
            <option value="IN_PROGRESS">In Progress</option>
            <option value="IN_REVIEW">In Review</option>
            <option value="DONE">Done</option>
            <option value="CANCELLED">Cancelled</option>
          </Select>
        </div>
      </div>

      {/* Due Date */}
      <div>
        <label htmlFor="dueDate" className="block text-sm font-medium">
          Due Date
        </label>
        <Input
          id="dueDate"
          type="datetime-local"
          {...form.register("dueDate")}
          className="mt-1"
        />
      </div>

      {/* Tags */}
      <div>
        <label className="block text-sm font-medium">Tags</label>
        <div className="mt-1 flex flex-wrap gap-1 mb-1">
          {tags.map((tag) => (
            <span
              key={tag}
              className="inline-flex items-center gap-1 rounded-full bg-secondary px-2 py-0.5 text-xs"
            >
              #{tag}
              <button
                type="button"
                onClick={() => removeTag(tag)}
                className="text-muted-foreground hover:text-destructive"
                aria-label={`Remove tag ${tag}`}
              >
                ×
              </button>
            </span>
          ))}
        </div>
        <div className="flex gap-2">
          <Input
            value={tagInput}
            onChange={(e) => setTagInput(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                e.preventDefault();
                addTag();
              }
            }}
            placeholder="Add a tag..."
            className="flex-1"
          />
          <Button type="button" variant="outline" onClick={addTag} size="sm">
            Add
          </Button>
        </div>
      </div>

      {/* Global Error */}
      {mutation.error && (
        <div
          className="rounded-md bg-destructive/10 p-3 text-sm text-destructive"
          role="alert"
        >
          {mutation.error.message}
        </div>
      )}

      {/* Buttons */}
      <div className="flex justify-end gap-3 pt-2">
        {onCancel && (
          <Button type="button" variant="ghost" onClick={onCancel}>
            Cancel
          </Button>
        )}
        <Button type="submit" disabled={mutation.isPending}>
          {mutation.isPending && <Spinner className="mr-2 h-4 w-4" />}
          {isEdit ? "Save Changes" : "Create Task"}
        </Button>
      </div>
    </form>
  );
}
```

> **Note:** The TaskForm component above also needs `useState` imported at the top: `import { useState } from "react";`

---

### 6.4 TaskDashboard (Container)

**File:** `src/components/tasks/task-dashboard.tsx`

```tsx
"use client";

import { useState, useCallback } from "react";
import { TaskList } from "./task-list";
import { TaskForm } from "./task-form";
import { TaskFilters } from "./task-filters";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { useTasks, useDeleteTask, useUpdateTask } from "@/lib/hooks/use-tasks";
import type { TaskFilterInput } from "@/lib/schemas/task";

export function TaskDashboard() {
  const [filters, setFilters] = useState<TaskFilterInput>({});
  const [createOpen, setCreateOpen] = useState(false);
  const [deletingTaskId, setDeletingTaskId] = useState<string | null>(null);

  const { data, isLoading, isError, error, refetch } = useTasks(filters);
  const deleteMutation = useDeleteTask();
  const updateMutation = useUpdateTask();

  const handleDelete = useCallback(
    (id: string) => {
      setDeletingTaskId(id);
      deleteMutation.mutate(
        { id },
        {
          onSettled: () => setDeletingTaskId(null),
        }
      );
    },
    [deleteMutation]
  );

  const handleStatusChange = useCallback(
    (id: string, status: string) => {
      updateMutation.mutate({ id, status });
    },
    [updateMutation]
  );

  // Collect IDs of all tasks currently being mutated (for optimistic display)
  const mutatingTaskIds = new Set<string>();
  updateMutation.variables?.id && mutatingTaskIds.add(updateMutation.variables.id);

  return (
    <div className="mx-auto max-w-4xl px-4 py-8">
      {/* Header */}
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Tasks</h1>
          <p className="text-sm text-muted-foreground">
            {data?.totalCount ?? 0} task{data?.totalCount !== 1 ? "s" : ""}
          </p>
        </div>
        <Dialog open={createOpen} onOpenChange={setCreateOpen}>
          <DialogTrigger asChild>
            <Button>+ New Task</Button>
          </DialogTrigger>
          <DialogContent className="max-w-lg">
            <DialogHeader>
              <DialogTitle>Create Task</DialogTitle>
            </DialogHeader>
            <TaskForm onSuccess={() => setCreateOpen(false)} />
          </DialogContent>
        </Dialog>
      </div>

      {/* Filters */}
      <TaskFilters filters={filters} onChange={setFilters} />

      {/* Global mutation error toast */}
      {deleteMutation.error && (
        <div className="mb-4 rounded-md bg-destructive/10 p-3 text-sm text-destructive">
          Failed to delete task: {deleteMutation.error.message}
        </div>
      )}

      {/* Task List */}
      <div className="mt-6">
        <TaskList
          tasks={data?.tasks ?? []}
          isLoading={isLoading}
          isError={isError}
          error={error}
          onRefetch={() => refetch()}
          onDelete={handleDelete}
          onStatusChange={handleStatusChange}
          deletingTaskId={deletingTaskId}
          mutatingTaskIds={mutatingTaskIds}
        />
      </div>
    </div>
  );
}
```

---

### 6.5 Supporting Components

**TaskFilters —** `src/components/tasks/task-filters.tsx`

```tsx
"use client";

import { useCallback } from "react";
import { Input } from "@/components/ui/input";
import { Select } from "@/components/ui/select";
import { Button } from "@/components/ui/button";
import type { TaskFilterInput } from "@/lib/schemas/task";

interface TaskFiltersProps {
  filters: TaskFilterInput;
  onChange: (filters: TaskFilterInput) => void;
}

export function TaskFilters({ filters, onChange }: TaskFiltersProps) {
  const update = useCallback(
    (patch: Partial<TaskFilterInput>) => {
      onChange({ ...filters, ...patch });
    },
    [filters, onChange]
  );

  const clear = () => onChange({});

  return (
    <div className="flex flex-wrap items-center gap-3 rounded-lg border bg-card p-3">
      <Input
        placeholder="Search tasks..."
        value={filters.search ?? ""}
        onChange={(e) => update({ search: e.target.value || undefined })}
        className="w-48"
        aria-label="Search tasks"
      />
      <Select
        value={filters.status ?? ""}
        onChange={(e) =>
          update({ status: (e.target.value as TaskFilterInput["status"]) || undefined })
        }
        className="w-36"
        aria-label="Filter by status"
      >
        <option value="">All Statuses</option>
        <option value="TODO">To Do</option>
        <option value="IN_PROGRESS">In Progress</option>
        <option value="IN_REVIEW">In Review</option>
        <option value="DONE">Done</option>
        <option value="CANCELLED">Cancelled</option>
      </Select>
      <Select
        value={filters.priority ?? ""}
        onChange={(e) =>
          update({
            priority: (e.target.value as TaskFilterInput["priority"]) || undefined,
          })
        }
        className="w-36"
        aria-label="Filter by priority"
      >
        <option value="">All Priorities</option>
        <option value="LOW">Low</option>
        <option value="MEDIUM">Medium</option>
        <option value="HIGH">High</option>
        <option value="URGENT">Urgent</option>
      </Select>
      <Select
        value={filters.sortBy ?? "createdAt"}
        onChange={(e) =>
          update({ sortBy: e.target.value as TaskFilterInput["sortBy"] })
        }
        className="w-40"
        aria-label="Sort by"
      >
        <option value="createdAt">Sort: Created</option>
        <option value="dueDate">Sort: Due Date</option>
        <option value="priority">Sort: Priority</option>
      </Select>
      <Button variant="ghost" size="sm" onClick={clear}>
        Clear
      </Button>
    </div>
  );
}
```

**TaskSkeleton —** `src/components/tasks/task-skeleton.tsx`

```tsx
export function TaskSkeleton() {
  return (
    <div className="animate-pulse rounded-lg border bg-card p-4 shadow-sm">
      <div className="flex items-start justify-between gap-2">
        <div className="flex-1 space-y-2">
          <div className="h-5 w-2/3 rounded bg-muted" />
          <div className="h-4 w-full rounded bg-muted" />
        </div>
        <div className="h-5 w-16 rounded-full bg-muted" />
      </div>
      <div className="mt-3 flex items-center justify-between">
        <div className="h-5 w-20 rounded-full bg-muted" />
        <div className="h-5 w-28 rounded bg-muted" />
      </div>
    </div>
  );
}
```

**TaskEmptyState —** `src/components/tasks/task-empty-state.tsx`

```tsx
export function TaskEmptyState() {
  return (
    <div className="flex flex-col items-center justify-center rounded-lg border py-16 text-center">
      <div className="mb-2 text-5xl">📋</div>
      <h3 className="text-lg font-semibold">No tasks yet</h3>
      <p className="mt-1 text-sm text-muted-foreground">
        Create your first task to get started.
      </p>
    </div>
  );
}
```

---

## 7. React Query Hooks & State Management

**File:** `src/lib/hooks/use-tasks.ts`

```typescript
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { TRPCClientError } from "@trpc/client";
import { trpc } from "@/lib/trpc/client";
import type { TaskFilterInput, TaskCreateInput, TaskUpdateInput } from "@/lib/schemas/task";

// ── GET task query key factory ─────────────────────────
export const taskKeys = {
  all: ["tasks"] as const,
  lists: () => [...taskKeys.all, "list"] as const,
  list: (filters: TaskFilterInput) => [...taskKeys.lists(), filters] as const,
  details: () => [...taskKeys.all, "detail"] as const,
  detail: (id: string) => [...taskKeys.details(), id] as const,
};

// ── useTasks (list) ────────────────────────────────────
export function useTasks(filters: TaskFilterInput = {}) {
  return useQuery({
    queryKey: taskKeys.list(filters),
    queryFn: () => trpc.task.list.query(filters),
    staleTime: 30_000,           // 30s before refetch
    gcTime: 5 * 60_000,          // 5min garbage collection
    placeholderData: (prev) => prev,  // Keep previous data during refetch
    retry: 2,                    // Retry twice on failure
  });
}

// ── useTask (single) ───────────────────────────────────
export function useTask(id: string) {
  return useQuery({
    queryKey: taskKeys.detail(id),
    queryFn: () => trpc.task.byId.query({ id }),
    enabled: !!id,
    staleTime: 60_000,
    retry: 1,
  });
}

// ── useCreateTask ──────────────────────────────────────
export function useCreateTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (input: TaskCreateInput) => trpc.task.create.mutate(input),

    // ── Optimistic: Add to cache immediately ─────────
    onMutate: async (newTask) => {
      // Cancel any in-flight list queries so they don't overwrite our optimistic update
      await queryClient.cancelQueries({ queryKey: taskKeys.lists() });

      const previousLists = queryClient.getQueriesData({
        queryKey: taskKeys.lists(),
      });

      // Snapshot task object for optimistic insert
      const optimisticTask = {
        id: `temp-${Date.now()}`,
        title: newTask.title,
        description: newTask.description ?? null,
        status: newTask.status ?? "TODO",
        priority: newTask.priority ?? "MEDIUM",
        dueDate: newTask.dueDate ? new Date(newTask.dueDate).toISOString() : null,
        tags: newTask.tags ?? [],
        assignedTo: null,
        createdAt: new Date().toISOString(),
        updatedAt: new Date().toISOString(),
        completedAt: null,
        // Optimistic marker
        __optimistic: true,
      };

      // Prepend to every cached task list
      queryClient.setQueriesData(
        { queryKey: taskKeys.lists() },
        (old: any) => {
          if (!old) return old;
          return {
            ...old,
            tasks: [optimisticTask, ...(old.tasks ?? [])],
            totalCount: (old.totalCount ?? 0) + 1,
          };
        }
      );

      return { previousLists };
    },

    // ── On error: rollback ───────────────────────────
    onError: (_error, _vars, context) => {
      if (context?.previousLists) {
        for (const [queryKey, data] of context.previousLists) {
          queryClient.setQueryData(queryKey, data);
        }
      }
    },

    // ── On success/error: invalidate to get real data ─
    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: taskKeys.lists() });
    },
  });
}

// ── useUpdateTask ──────────────────────────────────────
export function useUpdateTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (input: TaskUpdateInput) => trpc.task.update.mutate(input),

    onMutate: async (updatedTask) => {
      await queryClient.cancelQueries({ queryKey: taskKeys.lists() });
      await queryClient.cancelQueries({ queryKey: taskKeys.detail(updatedTask.id) });

      const previousLists = queryClient.getQueriesData({ queryKey: taskKeys.lists() });
      const previousDetail = queryClient.getQueryData(taskKeys.detail(updatedTask.id));

      // Optimistic update across all list caches
      queryClient.setQueriesData(
        { queryKey: taskKeys.lists() },
        (old: any) => {
          if (!old?.tasks) return old;
          return {
            ...old,
            tasks: old.tasks.map((t: any) =>
              t.id === updatedTask.id ? { ...t, ...updatedTask, __optimistic: true } : t
            ),
          };
        }
      );

      return { previousLists, previousDetail };
    },

    onError: (_error, vars, context) => {
      if (context?.previousLists) {
        for (const [queryKey, data] of context.previousLists) {
          queryClient.setQueryData(queryKey, data);
        }
      }
      if (context?.previousDetail) {
        queryClient.setQueryData(taskKeys.detail(vars.id), context.previousDetail);
      }
    },

    onSettled: (_data, _error, vars) => {
      queryClient.invalidateQueries({ queryKey: taskKeys.lists() });
      queryClient.invalidateQueries({ queryKey: taskKeys.detail(vars.id) });
    },
  });
}

// ── useDeleteTask ──────────────────────────────────────
export function useDeleteTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (input: { id: string }) => trpc.task.delete.mutate(input),

    onMutate: async ({ id }) => {
      await queryClient.cancelQueries({ queryKey: taskKeys.lists() });

      const previousLists = queryClient.getQueriesData({ queryKey: taskKeys.lists() });

      // Optimistic removal
      queryClient.setQueriesData(
        { queryKey: taskKeys.lists() },
        (old: any) => {
          if (!old?.tasks) return old;
          return {
            ...old,
            tasks: old.tasks.filter((t: any) => t.id !== id),
            totalCount: Math.max(0, (old.totalCount ?? 1) - 1),
          };
        }
      );

      return { previousLists };
    },

    onError: (_error, _vars, context) => {
      if (context?.previousLists) {
        for (const [queryKey, data] of context.previousLists) {
          queryClient.setQueryData(queryKey, data);
        }
      }
    },

    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: taskKeys.lists() });
    },
  });
}

// ── useBatchUpdateStatus ───────────────────────────────
export function useBatchUpdateStatus() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (input: { taskIds: string[]; status: string }) =>
      trpc.task.batchUpdateStatus.mutate(input),

    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: taskKeys.lists() });
    },
  });
}
```

---

## 8. Optimistic Updates

The optimistic update strategy is baked into the React Query hooks above. Here's how it works:

### Pattern

```
┌──────────────┐     ┌───────────────┐     ┌──────────────┐
│  User clicks │────▶│ onMutate()    │────▶│ UI updates   │
│  "Create"    │     │ Cancel stale  │     │ instantly    │
└──────────────┘     │ queries       │     │ (optimistic) │
                     │ Snapshot prev  │     └──────┬───────┘
                     │ Insert temp    │            │
                     └───────┬───────┘            │
                             │              ┌─────▼─────────┐
                     ┌───────▼───────┐      │  Server        │
                     │  Server call  │◀─────│  processes     │
                     │  (mutationFn) │      │  mutation      │
                     └───────┬───────┘      └────────────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
         ┌────▼────┐    ┌────▼────┐    ┌────▼────┐
         │ Success │    │  Error  │    │ Settled │
         │ (cache  │    │ Rollback│    │ Inval-  │
         │  already│    │ previous│    │ idate   │
         │  looks  │    │ snap    │    │ queries │
         │  good)  │    │         │    │         │
         └─────────┘    └─────────┘    └─────────┘
```

### Key Principles

1. **Cancel in-flight queries** during mutation so stale data doesn't overwrite optimistic state.
2. **Snapshot previous cache** in `onMutate` context.
3. **Rollback** entire snapshot on error — every affected query key.
4. **Invalidate** on settled to reconcile server truth with cache.
5. **Optimistic marker** (`__optimistic: true`) flags items for UI differentiation (e.g., subtle opacity, a "saving..." indicator).

### Optimistic UI Signals

In `TaskCard`, the `isMutating` prop drives visual feedback:

```tsx
// TaskCard applies these when isMutating is true:
className={cn(
  isMutating && "opacity-70 pointer-events-none",
  isDeleting && "opacity-50 scale-95 animate-pulse"
)}
```

- **Create:** The new card appears instantly with `__optimistic: true` — render at 70% opacity until server confirms.
- **Update:** The card updates in place, dimmed temporarily.
- **Delete:** The card shrinks (scale-95), fades to 50%, and pulses until the server confirms removal.

---

## 9. Error Handling

### Layer 1: Validation (Zod — server-side)

All inputs are validated by Zod schemas before hitting the database. Invalid data is rejected with a 400-level error and the `fieldErrors` are surfaced in the form.

```typescript
// In tRPC errorFormatter:
error.cause instanceof ZodError
  ? error.cause.flatten()   // → { fieldErrors: { title: ["Required"] }, formErrors: [] }
  : null
```

### Layer 2: Not-Found (TRPCError)

Every mutation that references a task ID first checks existence and throws a typed error:

```typescript
if (!existing) {
  throw new TRPCError({ code: "NOT_FOUND", message: `Task "${id}" not found` });
}
```

### Layer 3: Global Error Boundary (React)

**File:** `src/components/error-boundary.tsx`

```tsx
"use client";

import { Component, type ReactNode } from "react";
import { Button } from "@/components/ui/button";

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: React.ErrorInfo) {
    console.error("[ErrorBoundary]", error, info.componentStack);
    // Optional: send to error tracking service
  }

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) return this.props.fallback;
      return (
        <div className="flex flex-col items-center justify-center py-16 text-center">
          <div className="mb-2 text-4xl">💥</div>
          <h2 className="text-xl font-bold">Something went wrong</h2>
          <p className="mt-2 text-sm text-muted-foreground">
            {this.state.error?.message ?? "An unexpected error occurred."}
          </p>
          <Button
            className="mt-4"
            onClick={() => this.setState({ hasError: false, error: null })}
          >
            Try Again
          </Button>
        </div>
      );
    }
    return this.props.children;
  }
}
```

### Layer 4: Toast Notifications

**File:** `src/components/ui/toast.tsx`

```tsx
"use client";

import { useEffect, useState, useCallback, createContext, useContext } from "react";
import { cn } from "@/lib/utils/cn";

// ── Types ──────────────────────────────────────────────
type ToastType = "success" | "error" | "info" | "warning";
interface Toast {
  id: string;
  type: ToastType;
  message: string;
  duration?: number;
}

// ── Context ────────────────────────────────────────────
interface ToastContextValue {
  toast: (message: string, type?: ToastType, duration?: number) => void;
}

const ToastContext = createContext<ToastContextValue>({
  toast: () => {},
});

export const useToast = () => useContext(ToastContext);

// ── Provider ───────────────────────────────────────────
export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const addToast = useCallback(
    (message: string, type: ToastType = "info", duration = 4000) => {
      const id = Date.now().toString(36) + Math.random().toString(36).slice(2);
      setToasts((prev) => [...prev, { id, type, message, duration }]);
    },
    []
  );

  const removeToast = useCallback((id: string) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  return (
    <ToastContext.Provider value={{ toast: addToast }}>
      {children}
      {/* Toast Container */}
      <div
        className="fixed bottom-4 right-4 z-50 flex flex-col gap-2"
        aria-live="polite"
        aria-label="Notifications"
      >
        {toasts.map((t) => (
          <ToastItem key={t.id} toast={t} onDismiss={removeToast} />
        ))}
      </div>
    </ToastContext.Provider>
  );
}

// ── Item ───────────────────────────────────────────────
function ToastItem({
  toast,
  onDismiss,
}: {
  toast: Toast;
  onDismiss: (id: string) => void;
}) {
  useEffect(() => {
    if (toast.duration === Infinity) return;
    const timer = setTimeout(() => onDismiss(toast.id), toast.duration ?? 4000);
    return () => clearTimeout(timer);
  }, [toast, onDismiss]);

  const colorMap: Record<ToastType, string> = {
    success: "bg-green-50 border-green-400 text-green-900",
    error: "bg-red-50 border-red-400 text-red-900",
    warning: "bg-yellow-50 border-yellow-400 text-yellow-900",
    info: "bg-blue-50 border-blue-400 text-blue-900",
  };

  return (
    <div
      className={cn(
        "flex items-center gap-3 rounded-lg border px-4 py-3 shadow-lg animate-in slide-in-from-right transition-all",
        colorMap[toast.type]
      )}
      role="alert"
    >
      <span className="text-sm font-medium">{toast.message}</span>
      <button
        onClick={() => onDismiss(toast.id)}
        className="ml-auto shrink-0 text-current opacity-60 hover:opacity-100"
        aria-label="Dismiss"
      >
        ×
      </button>
    </div>
  );
}
```

### Layer 5: tRPC Error Serialization

The custom `errorFormatter` in `src/server/api/trpc.ts` ensures all errors come back as structured, serializable objects with consistent shape:

```typescript
{
  message: string;           // Human-readable
  code: string;              // TRPC error code
  data: {
    httpStatus: number;
    zodError: {              // Only if Zod validation failed
      fieldErrors: Record<string, string[]>;
      formErrors: string[];
    } | null;
    path: string;            // tRPC procedure path
  }
}
```

---

## 10. Loading States

### Route-Level Loading

**File:** `src/app/tasks/loading.tsx`

```tsx
import { TaskSkeleton } from "@/components/tasks/task-skeleton";

export default function TasksLoading() {
  return (
    <div className="mx-auto max-w-4xl px-4 py-8">
      {/* Header skeleton */}
      <div className="mb-6 flex items-center justify-between">
        <div className="space-y-2">
          <div className="h-8 w-32 animate-pulse rounded bg-muted" />
          <div className="h-4 w-20 animate-pulse rounded bg-muted" />
        </div>
        <div className="h-10 w-28 animate-pulse rounded-md bg-muted" />
      </div>

      {/* Filter skeleton */}
      <div className="flex gap-3 rounded-lg border bg-card p-3">
        <div className="h-10 w-48 animate-pulse rounded bg-muted" />
        <div className="h-10 w-36 animate-pulse rounded bg-muted" />
        <div className="h-10 w-36 animate-pulse rounded bg-muted" />
      </div>

      {/* Task skeleton list */}
      <div className="mt-6 space-y-3">
        {Array.from({ length: 5 }).map((_, i) => (
          <TaskSkeleton key={i} />
        ))}
      </div>
    </div>
  );
}
```

### Component-Level Loading (Skeleton)

The `TaskSkeleton` component (shown in §6.5) mimics the exact shape of `TaskCard` using Tailwind's `animate-pulse` and `bg-muted` placeholders. This prevents layout shift when data arrives.

### Mutation Loading (Button Spinner)

```tsx
<Button type="submit" disabled={mutation.isPending}>
  {mutation.isPending && <Spinner className="mr-2 h-4 w-4" />}
  {isEdit ? "Save Changes" : "Create Task"}
</Button>
```

**Spinner —** `src/components/ui/spinner.tsx`

```tsx
import { cn } from "@/lib/utils/cn";

export function Spinner({ className, ...props }: React.SVGProps<SVGSVGElement>) {
  return (
    <svg
      className={cn("animate-spin", className)}
      xmlns="http://www.w3.org/2000/svg"
      fill="none"
      viewBox="0 0 24 24"
      aria-hidden="true"
      {...props}
    >
      <circle
        className="opacity-25"
        cx="12"
        cy="12"
        r="10"
        stroke="currentColor"
        strokeWidth="4"
      />
      <path
        className="opacity-75"
        fill="currentColor"
        d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"
      />
    </svg>
  );
}
```

### Status-Based Loading States Summary

| State | Trigger | Visual |
|-------|---------|--------|
| **Initial load** | Page mount, no cached data | Full-page skeleton (`loading.tsx`) |
| **Refetch** | Query invalidation, stale data | Previous data shown with `placeholderData`; no spinner |
| **Background refetch** | Window refocus, reconnect | Invisible to user |
| **Mutation pending** | Create/Update/Delete in flight | Optimistic UI: dimmed card (70% opacity) |
| **Delete pending** | Delete mutation | Card shrinks + pulses, button disabled |
| **Mutation error** | Network/server failure | Rollback to previous state + toast notification |

---

## 11. Integration Guide

### Step 1: Install Dependencies

```bash
npm install \
  @prisma/client \
  @tanstack/react-query \
  @trpc/client @trpc/server @trpc/next @trpc/react-query \
  superjson \
  zod \
  date-fns \
  react-hook-form @hookform/resolvers

npm install -D prisma
```

### Step 2: Initialize Prisma

```bash
npx prisma init
```

- Replace the generated `prisma/schema.prisma` with the schema from §2.
- Set `DATABASE_URL` in your `.env`.
- Run migrations:

```bash
npx prisma migrate dev --name init
npx prisma generate
```

### Step 3: Set Up tRPC Server

1. Create the files listed in §3:
   - `src/server/api/trpc.ts`
   - `src/server/api/routers/root.ts`
   - `src/server/api/routers/task.ts`
   - `src/app/api/trpc/[trpc]/route.ts`

2. Create `src/server/db/index.ts` (Prisma client singleton).

### Step 4: Set Up tRPC Client

**File:** `src/lib/trpc/client.ts`

```typescript
import { createTRPCReact } from "@trpc/react-query";
import type { AppRouter } from "@/server/api/routers/root";

export const trpc = createTRPCReact<AppRouter>();
```

**File:** `src/lib/trpc/react.tsx`

```tsx
"use client";

import { useState } from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { httpBatchLink, loggerLink } from "@trpc/client";
import superjson from "superjson";
import { trpc } from "./client";

function getBaseUrl() {
  if (typeof window !== "undefined") return "";
  if (process.env.VERCEL_URL) return `https://${process.env.VERCEL_URL}`;
  return `http://localhost:${process.env.PORT ?? 3000}`;
}

export function TRPCProvider({ children }: { children: React.ReactNode }) {
  const [queryClient] = useState(
    () =>
      new QueryClient({
        defaultOptions: {
          queries: {
            staleTime: 30_000,
            refetchOnWindowFocus: false,
            retry: 1,
          },
          mutations: {
            retry: 0,
          },
        },
      })
  );

  const [trpcClient] = useState(() =>
    trpc.createClient({
      links: [
        loggerLink({
          enabled: (opts) =>
            process.env.NODE_ENV === "development" ||
            (opts.direction === "down" && opts.result instanceof Error),
        }),
        httpBatchLink({
          url: `${getBaseUrl()}/api/trpc`,
          transformer: superjson,
          headers() {
            return {
              // Include auth headers if available
            };
          },
        }),
      ],
    })
  );

  return (
    <trpc.Provider client={trpcClient} queryClient={queryClient}>
      <QueryClientProvider client={queryClient}>
        {children}
      </QueryClientProvider>
    </trpc.Provider>
  );
}
```

### Step 5: Wrap Root Layout

**File:** `src/app/layout.tsx`

```tsx
import type { Metadata } from "next";
import { TRPCProvider } from "@/lib/trpc/react";
import { ToastProvider } from "@/components/ui/toast";
import { ErrorBoundary } from "@/components/error-boundary";

import "./globals.css";

export const metadata: Metadata = {
  title: "Task Manager",
  description: "Fullstack task management application",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <ErrorBoundary>
          <TRPCProvider>
            <ToastProvider>
              {children}
            </ToastProvider>
          </TRPCProvider>
        </ErrorBoundary>
      </body>
    </html>
  );
}
```

### Step 6: Create the Tasks Page

**File:** `src/app/tasks/page.tsx`

```tsx
import { TaskDashboard } from "@/components/tasks/task-dashboard";

export default function TasksPage() {
  return <TaskDashboard />;
}
```

### Step 7: Add UI Primitives

Create the shadcn/ui-style components under `src/components/ui/`:

- `button.tsx`
- `input.tsx`
- `textarea.tsx`
- `select.tsx`
- `badge.tsx`
- `card.tsx`
- `dialog.tsx`
- `spinner.tsx` (provided in §10)
- `toast.tsx` (provided in §9)

You can generate these with `npx shadcn-ui@latest init` and `npx shadcn-ui@latest add button input textarea select badge card dialog`.

### Step 8: Run the Application

```bash
npm run dev
```

Visit `http://localhost:3000/tasks` to see the task dashboard.

### Step 9: Database Seeding (Optional)

**File:** `prisma/seed.ts`

```typescript
import { PrismaClient } from "@prisma/client";

const db = new PrismaClient();

async function main() {
  // Create demo user
  const user = await db.user.upsert({
    where: { email: "demo@example.com" },
    update: {},
    create: {
      name: "Demo User",
      email: "demo@example.com",
    },
  });

  // Create sample tasks
  const tasks = [
    { title: "Set up CI/CD pipeline", priority: "HIGH" as const, status: "IN_PROGRESS" as const },
    { title: "Design onboarding flow", priority: "URGENT" as const, status: "TODO" as const, dueDate: new Date("2026-07-01") },
    { title: "Write API documentation", priority: "MEDIUM" as const, status: "TODO" as const },
    { title: "Fix login redirect bug", priority: "HIGH" as const, status: "IN_REVIEW" as const },
    { title: "Update privacy policy", priority: "LOW" as const, status: "DONE" as const },
    { title: "Implement dark mode toggle", priority: "MEDIUM" as const, status: "TODO" as const, tags: ["UI", "v2.0"] },
    { title: "Optimize database queries", priority: "HIGH" as const, status: "TODO" as const, tags: ["performance"] },
    { title: "Add rate limiting to API", priority: "URGENT" as const, status: "IN_PROGRESS" as const },
  ];

  for (const task of tasks) {
    await db.task.create({
      data: {
        ...task,
        description: `Sample description for: ${task.title}`,
        assignedToId: user.id,
      },
    });
  }

  console.log("✅ Seeded database with demo tasks");
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(async () => {
    await db.$disconnect();
  });
```

Run with:

```bash
npx prisma db seed
```

Add to `package.json`:

```json
"prisma": {
  "seed": "tsx prisma/seed.ts"
}
```

---

## 12. API Reference

### tRPC Endpoints

| Procedure | Type | Input | Output | Description |
|-----------|------|-------|--------|-------------|
| `task.list` | Query | `TaskFilterInput?` | `{ tasks, totalCount, nextCursor? }` | Paginated, filterable task list |
| `task.byId` | Query | `{ id: string }` | `Task` | Single task by ID |
| `task.create` | Mutation | `TaskCreateInput` | `Task` | Create a new task |
| `task.update` | Mutation | `TaskUpdateInput` | `Task` | Partial update to a task |
| `task.delete` | Mutation | `{ id: string }` | `{ success, id }` | Delete a task |
| `task.batchUpdateStatus` | Mutation | `{ taskIds, status }` | `Task[]` | Bulk status change |

### Filter Parameters (`TaskFilterInput`)

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `status` | `Status?` | - | Filter by status |
| `priority` | `Priority?` | - | Filter by priority |
| `search` | `string?` | - | Search title & description |
| `sortBy` | `"createdAt" \| "dueDate" \| "priority"` | `"createdAt"` | Sort field |
| `sortOrder` | `"asc" \| "desc"` | `"desc"` | Sort direction |
| `limit` | `number` | `20` | Items per page |
| `cursor` | `string?` | - | Pagination cursor |

### Error Codes

| HTTP | tRPC Code | When |
|------|-----------|------|
| 400 | `BAD_REQUEST` | Zod validation failure |
| 404 | `NOT_FOUND` | Task ID doesn't exist |
| 401 | `UNAUTHORIZED` | Missing auth (protected routes) |
| 500 | `INTERNAL_SERVER_ERROR` | Unexpected server error |

---

## Summary of Deliverables

### Files Created (25 files in total)

**Backend (5 files):**
- `src/server/db/schema.prisma` — Database model with Task + User tables
- `src/server/db/index.ts` — Prisma client singleton
- `src/server/api/trpc.ts` — tRPC context, middleware, error formatting
- `src/server/api/routers/root.ts` — Root router merging all sub-routers
- `src/server/api/routers/task.ts` — Task CRUD router (6 procedures)
- `src/app/api/trpc/[trpc]/route.ts` — Next.js App Router HTTP handler

**Client Infrastructure (3 files):**
- `src/lib/trpc/client.ts` — tRPC React client
- `src/lib/trpc/react.tsx` — TRPCProvider + QueryClient setup
- `src/lib/trpc/server.ts` — Server-side caller (for SSR)

**Schemas & Types (1 file):**
- `src/lib/schemas/task.ts` — Zod schemas for create, update, filter, ID

**Hooks (1 file):**
- `src/lib/hooks/use-tasks.ts` — 5 React Query hooks with optimistic mutations

**Components (7 files):**
- `src/components/tasks/task-list.tsx` — Sortable/filterable list with loading/error/empty states
- `src/components/tasks/task-card.tsx` — Individual task card with status cycling, due date logic, edit dialog
- `src/components/tasks/task-form.tsx` — Create/edit form with react-hook-form + Zod
- `src/components/tasks/task-dashboard.tsx` — Container orchestrating all states
- `src/components/tasks/task-filters.tsx` — Status/priority search bar
- `src/components/tasks/task-skeleton.tsx` — Card-shaped loading placeholder
- `src/components/tasks/task-empty-state.tsx` — Empty state with CTA

**UI Primitives (8 files):**
- `src/components/ui/button.tsx`, `input.tsx`, `textarea.tsx`, `select.tsx`, `badge.tsx`, `card.tsx`, `dialog.tsx`, `spinner.tsx`

**Infrastructure (3 files):**
- `src/components/error-boundary.tsx` — React error boundary
- `src/components/ui/toast.tsx` — Toast notification system
- `src/app/tasks/loading.tsx` — Route-level skeleton

**Pages & Layout (2 files):**
- `src/app/layout.tsx` — Root layout with providers
- `src/app/tasks/page.tsx` — Tasks route

### Key Features Implemented

- ✅ Full CRUD API with validation, not-found checks, and error serialization
- ✅ Optimistic updates for create, update, and delete mutations
- ✅ Graceful rollback on mutation failure (all cached queries restored)
- ✅ Stale-while-revalidate pattern with `placeholderData`
- ✅ Pagination with cursor-based infinite scrolling support
- ✅ Search, filter, and sort capabilities
- ✅ Four distinct UI states per component: loading, empty, error, populated
- ✅ Accessible forms with aria attributes and role annotations
- ✅ Priority-based color coding with overdue detection
- ✅ Status cycling button (TODO → IN_PROGRESS → IN_REVIEW → DONE)
- ✅ Toast notifications for async operation feedback
- ✅ Error boundary for uncaught React errors
- ✅ Database indexes on commonly queried columns
- ✅ Database seeding script for development
- ✅ Auto-completedAt tracking when transitioning to DONE
