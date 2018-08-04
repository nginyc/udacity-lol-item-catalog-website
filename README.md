# League of Legends Item Catalog

## Database Schema

### item
- `id` - Integer, PK
- `name` - String
- `description` - String
- `category_id` - String, FK
- `owner_id` - String, FK 

### item_catagory
- `id` - Integer, PK
- `name` - String

### user
- `id` - Integer, PK
- `name` - String
- `profile_image_url` - String
- `email` - String, Unique
