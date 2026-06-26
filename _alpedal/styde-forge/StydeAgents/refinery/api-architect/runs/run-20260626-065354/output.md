I see the current Styde Forge API. It runs on Python http.server, has 6 POST endpoints and 4 GET endpoints. No versioning, no auth, no schema, no documentation. Below is an OpenAPI 3.0 spec for the entire existing API surface.
openapi: 3.0.3
info:
  title: Styde Forge API
  version: 1.0.0
  description: Mission Control API for Styde Forge agent factory. Manages spawn, eval, improve, and forge loop operations. Backend: Python http.server, port 8765.
servers:
  - url: http://localhost:8765
    description: Local forge dashboard
paths:
  /api/state:
    get:
      summary: Full forge dashboard state
      operationId: getState
      responses:
        '200':
          description: Aggregate dashboard payload
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/DashboardState'
  /api/state.yaml:
    get:
      summary: Raw state.yaml file
      operationId: getRawState
      responses:
        '200':
          description: Raw YAML file content
          content:
            text/yaml:
              schema:
                type: string
  /api/skills:
    get:
      summary: Skill inventory (refinery scans)
      operationId: getSkills
      responses:
        '200':
          description: List of discovered skills
          content:
            application/json:
              schema:
                type: object
              properties:
                skills:
                  type: array
                  items:
                    $ref: '#/components/schemas/Skill'
  /api/activity:
    get:
      summary: Activity feed (last 50 entries)
      operationId: getActivity
      responses:
        '200':
          description: Activity log entries
          content:
            application/json:
              schema:
                type: object
                properties:
                  activity:
                    type: array
                    items:
                      $ref: '#/components/schemas/ActivityEntry'
  /api/spawn:
    post:
      summary: Spawn a new agent from a blueprint
      operationId: spawnAgent
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - blueprint
              properties:
                blueprint:
                  type: string
                  description: Blueprint name (directory under StydeAgents/refinery/)
                  example: api-gateway-designer
      responses:
        '200':
          description: Spawn accepted (runs async)
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AckResponse'
  /api/eval:
    post:
      summary: Run evaluation on a blueprint run
      operationId: evalRun
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - blueprint
              properties:
                blueprint:
                  type: string
                run_id:
                  type: string
                  default: latest
                  description: Specific run directory ID, or 'latest'
      responses:
        '200':
          description: Eval accepted
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AckResponse'
  /api/improve:
    post:
      summary: Improve an existing run via teacher feedback
      operationId: improveRun
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - blueprint
                - run_id
              properties:
                blueprint:
                  type: string
                run_id:
                  type: string
      responses:
        '200':
          description: Improvement accepted
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AckResponse'
  /api/toggle-caveman:
    post:
      summary: Toggle Caveman Ultra mode on/off
      operationId: toggleCaveman
      requestBody:
        content:
          application/json:
            schema:
              type: object
      responses:
        '200':
          description: Caveman mode toggled in state.yaml
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AckResponse'
  /api/loop:
    post:
      summary: Start forge auto-loop (spawn -> eval -> improve cycle)
      operationId: startForgeLoop
      requestBody:
        content:
          application/json:
            schema:
              type: object
      responses:
        '200':
          description: Loop started
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/AckResponse'
components:
  schemas:
    AckResponse:
      type: object
      properties:
        ok:
          type: boolean
          default: true
        error:
          type: string
          description: Present only on 404 or failure
    DashboardState:
      type: object
      properties:
        forge:
          type: object
          properties:
            codename:
              type: string
            version:
              type: string
            loop_iterations:
              type: integer
            total_agents:
              type: integer
            total_evaluations:
              type: integer
            caveman_ultra:
              type: boolean
            last_checkpoint:
              type: string
            is_working:
              type: boolean
        pipeline:
          type: object
          properties:
            refinery:
              type: integer
            production:
              type: integer
            archive:
              type: integer
        agents:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
              blueprint:
                type: string
              stage:
                type: string
              composite_score:
                type: number
                nullable: true
        hardware:
          type: object
          properties:
            gpus:
              type: array
              items:
                type: object
                properties:
                  index:
                    type: string
                  name:
                    type: string
                  vram_total_mb:
                    type: string
                  vram_used_mb:
                    type: string
                  vram_free_mb:
                    type: string
                  load_pct:
                    type: string
                  temp_c:
                    type: string
                  power_w:
                    type: string
            ram:
              type: string
            cpu:
              type: string
            python:
              type: string
        skills:
          type: array
          items:
            $ref: '#/components/schemas/Skill'
        activity:
          type: array
          items:
            $ref: '#/components/schemas/ActivityEntry'
    Skill:
      type: object
      properties:
        name:
          type: string
        runs:
          type: array
          items:
            type: object
            properties:
              id:
                type: string
              score:
                type: number
                nullable: true
              task:
                type: string
              output_preview:
                type: string
        latest_score:
          type: number
          nullable: true
        stage:
          type: string
          enum:
            - refinery
            - production
            - archive
        version:
          type: string
    ActivityEntry:
      type: object
      properties:
        id:
          type: integer
        action:
          type: string
          enum:
            - spawn
            - eval
            - improve
            - loop
            - config
        blueprint:
          type: string
        detail:
          type: string
        progress:
          type: integer
        status:
          type: string
          enum:
            - pending
            - running
            - complete
            - failed
        timestamp:
          type: string
          format: date-time
design_notes:
  - endpoint: All POST endpoints return {'ok': True} immediately then run async via subprocess.Popen. No job ID or status polling mechanism exists.
  - missing_rate_limits: No rate limiting on any endpoint. Server is single-threaded HTTPServer.
  - no_auth: Intra-network only. No API keys, no authentication.
  - no_versioning: No /v1/ prefix. Toggle-caveman is an ad-hoc config endpoint on the state file.
  - error_response: 404 returns plain text 'Not found'. No structured error body.
  - cors: '*' origin, no credential cookies.
  - idempotency: POST /api/spawn with same blueprint launches a new subprocess each time, no dedup.
  - recommendation: v2 redesign should add job IDs, polling endpoint /api/jobs/{id}, and structured error schema.