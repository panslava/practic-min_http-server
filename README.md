## Simple socket server, with mongodb and redis cache

``start: docker-compose up``

``build: docker-compose build``

### endpoints:

- `/put POST, PUT `

    Create or update value by key
    
    *Request parameters*:
    
    - **key** - *string*
    
    - **value** - *any*
  
- `/get GET`

    Get value by key
    
    *Request parameters*:
    
    - **key** - *string*
    
    - **no-cache** - *boolean* optional
    
- `/delete DELETE`

    Delete by key
    
    *Request parameters*:
    
    - **key** - *string*
