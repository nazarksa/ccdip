PRODUCT_SPEC.md
      │
      ├── What problem are we solving?
      ├── Who uses it?
      ├── What is a Project?
      ├── What is a Supplier?
      ├── What does "causality" mean?
      ├── What relationships exist?
      ├── What can AI claim?
      ├── What can AI NOT claim?
      ├── How is evidence represented?
      └── What does "production-ready" mean?
                │
                ↓
        Cursor implementation
                │
       ┌────────┼─────────┐
       ↓        ↓         ↓
 PostgreSQL   Neo4j    LangGraph
       │        │         │
       └────────┼─────────┘
                ↓
             React