# Git Workflow — styde.ai

Simple. Two people. One repo. No branches (yet).

## Quick Reference

```bash
git pull                    # Always start here — get latest
git status                  # What changed?
git add -A                  # Stage everything
git commit -m "message"     # Save locally
git push                    # Send to GitHub
```

## Daily Flow

### William (repo owner)

```
git pull                    # Get Alpedal's changes
# ... work in _william/, apps/, obsidian/ ...
git add -A
git commit -m "what you did"
git push
```

### Alpedal (collaborator)

**First time only:**
```
git clone https://github.com/dopaminedotmd/styde.git
cd styde
```

**Every session:**
```
git pull                    # Get William's changes
# ... work in _alpedal/, agent-blueprints/ ...
git add -A
git commit -m "blueprint: invoice-reviewer v0.1"
git push
```

## Who Touches What

| Folder | Owner | Rule |
|--------|-------|------|
| `_william/` | William | Only William |
| `_alpedal/` | Alpedal | Only Alpedal |
| `apps/` | William | William builds code here |
| `agent-blueprints/` | Alpedal → William review | Alpedal creates, both approve |
| `obsidian/` | Both | William owns the plan |
| `skills/` | Hermes (bot) | Auto-managed |

**Golden rule:** Never touch each other's `_` folders. For everything else — pull before you push.

## If Something Goes Wrong

```bash
# "I messed up my local files"
git stash                   # Hide your changes temporarily
git pull                    # Get clean version
git stash pop               # Bring your changes back

# "I want to undo my last commit (not pushed yet)"
git reset --soft HEAD~1     # Undo commit, keep changes

# "I have no idea what's happening"
git status                  # Always tells you where you are
```

## Commit Messages

Keep them short. Format:

```
what: short description
```

Examples:
```
blueprint: invoice-reviewer v0.1
fix: consultant agent timeout bug  
feat: added PDF export to konsult.py
docs: updated MASTER_PLAN.md
```
