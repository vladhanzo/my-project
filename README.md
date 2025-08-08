erDiagram
    PRODUCT_MODEL {
        UUID id PK
        TEXT name
        TEXT description
    }
    ASSEMBLY {
        UUID id PK
        UUID product_model_id FK
        TEXT serial_number
        TIMESTAMP created_at
    }
    OPERATION {
        UUID id PK
        UUID product_model_id FK
        TEXT name
        INT sequence
        TEXT description
    }
    COMPONENT {
        UUID id PK
        TEXT name
        TEXT part_number
        JSONB specification
    }
    ASSEMBLER {
        UUID id PK
        TEXT name
        TEXT employee_id
    }
    COMPONENT_ACTION {
        UUID id PK
        UUID assembly_id FK
        UUID operation_id FK
        UUID component_id FK
        UUID assembler_id FK
        TIMESTAMP performed_at
        TEXT notes
    }

    PRODUCT_MODEL ||--o{ ASSEMBLY          : has
    PRODUCT_MODEL ||--o{ OPERATION         : defines
    ASSEMBLY      ||--o{ COMPONENT_ACTION : "records"
    OPERATION     ||--o{ COMPONENT_ACTION : "executes"
    COMPONENT     ||--o{ COMPONENT_ACTION : "uses"
    ASSEMBLER     ||--o{ COMPONENT_ACTION : "performs"

erDiagram
    PRODUCT_SERIES ||--o{ PRODUCT_MODEL : has
    PRODUCT_MODEL ||--o{ MODEL_REVISION : has
    MODEL_REVISION ||--o{ REQUIRED_COMPONENT : requires
