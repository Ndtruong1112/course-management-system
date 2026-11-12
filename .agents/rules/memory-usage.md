# External Memory (Knowledge Graph) Integration

This project uses an external Knowledge Graph Memory MCP Server (`@modelcontextprotocol/server-memory`) to save tokens and maintain persistent long-term memory across sessions.

## Storage Location
- Graph file: `memory.json` in project root (`C:\Users\24110\Downloads\course-management-system--master\memory.json`).

## Token-Saving & Recall Guidelines:
1. **Search Before Re-reading Code**: When checking architecture, relationships, module designs, or past decisions, use `search_nodes` or `open_nodes` from the `memory` MCP server before reading multiple source files.
2. **Record Major Changes**: When adding new entities, modules, endpoints, or architectural decisions, record them using `create_entities`, `create_relations`, or `add_observations` so future turns can access them immediately without wasting context tokens.
