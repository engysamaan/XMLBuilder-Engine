# XMLBuilder Engine — Dynamic XML Generation & Data Transformation Framework

XMLBuilder Engine is a Python framework that automates the creation of complex, multi-layer XML documents from relational databases or dictionary-based datasets. It supports dynamic XML tree manipulation, schema-based node insertion, contract-like data transformation, and automated XML assembly used across various enterprise systems.

This toolkit was designed to generate structured XML configurations for multiple product categories, contract types, and business schemas — without being tied to any single use case.

---

## 🚀 Core Features

### 🧱 **1. Dynamic XML Construction**
- Build multi-level XML trees programmatically
- Convert DataFrames or dictionaries into XML elements
- Support for custom parent/child tag names
- Reusable utilities for merging, wrapping, and inserting XML nodes
- Fully schema-agnostic — supports any XML layout

### 🛠 **2. Advanced XML Utilities**
Included utility functions:

| Function | Description |
|---------|-------------|
| `convert2XML()` | Converts dictionaries or DataFrames to XML (using `dicttoxml`), cleans tags, outputs as element or file |
| `insert_xmltree()` | Inserts XML blocks inside other XML nodes at specific positions |
| `append_xmltree()` | Appends canonicalized XML into a destination XML file |
| `node_wrapper()` | Wraps XML fragments inside custom parent/end tags |

These utilities form the pipeline that builds complete XML documents from multiple partial fragments.

---

## 📊 **3. Data Transformation Layer**
- Converts raw DB query results into structured objects
- Maps boolean or numeric values into readable XML-compatible flags
- Cleans strings, removes unwanted characters, standardizes formats
- Generates nested product-like structures dynamically
- Summarizes numeric lists into ranges via the `SummarizeRange` class  
  - Example: `"1,2,3,7,8"` → `"1-3,7-8"`

---

## 🧩 **4. Supports Any Contract or Configuration Schema**
Although originally used for contract-style product structures, XMLBuilder Engine is built to support:

- Pricing and configuration XML  
- Authorization or policy XML  
- Catalog or product hierarchy XML  
- Data migration XML  
- Integration or trigger-based XML  
- Mapping or classification XML  

No schema hard-coded → fully reusable.

---

## 🔌 **5. Database-Driven Architecture**
- Accepts ProfileID or any key input
- Executes SQL queries to retrieve:
  - Customer groups
  - Authorization codes
  - Product lists
  - Attribute metadata
  - Any contract or configuration detail
- Dynamically transforms query results into XML fragments

---

                      ┌───────────────────────────────┐
                      │            INPUTS              │
                      │───────────────────────────────│
                      │  • SQL Database Tables         │
                      │  • JSON Config (ProfileID)     │
                      │  • DataFrames / Dictionaries   │
                      └───────────────┬───────────────┘
                                      │
                                      ▼
                 ┌──────────────────────────────────────────┐
                 │      1) DATA EXTRACTION LAYER            │
                 │──────────────────────────────────────────│
                 │ • Execute parameterized SQL queries      │
                 │ • Fetch groups, codes, products, attrs   │
                 │ • Convert results to pandas DataFrames   │
                 └───────────────┬──────────────────────────┘
                                 │
                                 ▼
                 ┌──────────────────────────────────────────┐
                 │      2) DATA TRANSFORMATION LAYER         │
                 │──────────────────────────────────────────│
                 │ • Clean / normalize values               │
                 │ • Generate flags (show/hide fields)      │
                 │ • Map 0/1 → readable XML values          │
                 │ • Summarize numeric ranges               │
                 │ • Build product + attribute dicts        │
                 └───────────────┬──────────────────────────┘
                                 │
                                 ▼
                 ┌──────────────────────────────────────────┐
                 │  3) XML FRAGMENT GENERATION (convert2XML) │
                 │──────────────────────────────────────────│
                 │ • Convert DF or dict → XML string        │
                 │ • Clean unwanted tags (<item>, <n0>…)    │
                 │ • Output as ElementTree or write to file │
                 └───────────────┬──────────────────────────┘
                                 │
                                 ▼
        ┌──────────────────────────────────────────────────────────────┐
        │  4) XML TREE CONSTRUCTION (insert_xmltree, append_xmltree)  │
        │──────────────────────────────────────────────────────────────│
        │ • Insert XML fragments into parent nodes                    │
        │ • Create nested child structures (e.g., Product lists)      │
        │ • Append intermediate XML blocks into a master XML file     │
        └───────────────┬────────────────────────────────────────────┘
                         │
                         ▼
        ┌──────────────────────────────────────────────────────────────┐
        │     5) XML WRAPPING (node_wrapper)                           │
        │──────────────────────────────────────────────────────────────│
        │ • Surround merged XML with <Parent> ... </Parent> tags       │
        │ • Finalize schema-based layout                               │
        └───────────────┬────────────────────────────────────────────┘
                         │
                         ▼
             ┌──────────────────────────────────────────────────┐
             │          FINAL OUTPUT XML FILE                   │
             │──────────────────────────────────────────────────│
             │ • Fully assembled XML                             │
             │ • Ready for AMS triggers / downstream systems     │
             │ • Schema-agnostic: supports any product/category  │
             └──────────────────────────────────────────────────┘





