# Resource Design - Thu vien

## ERD

- Book N:M Author (qua book_authors)
- Book N:1 Category
- Book 1:N Review (nested)

## Endpoints

| Method | URL | Mo ta |
|--------|-----|-------|
| GET | /api/v1/books | list books (paginate) |
| GET | /api/v1/books/{id} | chi tiet book |
| GET | /api/v1/books/{id}/reviews | reviews cua book |
| POST | /api/v1/books/{id}/reviews | them review |
| GET | /api/v1/books/{id}/authors | authors cua book |
| POST | /api/v1/books/{id}/authors | gan author |
| DELETE | /api/v1/books/{id}/authors/{aid} | go author |
| GET | /api/v1/authors | list authors |
| GET | /api/v1/authors/{id} | chi tiet author |
| GET | /api/v1/authors/{id}/books | sach cua author |
| GET | /api/v1/categories | list categories |
| GET | /api/v1/users/{id}/loans | lich su muon |
| POST | /api/v1/loans | tao phieu muon |
| POST | /api/v1/books | tao sach |
| PUT | /api/v1/books/{id} | update sach |
| DELETE | /api/v1/books/{id} | xoa sach |

## Query params list books

- strategy=offset|cursor
- limit, offset, cursor
- sort=-price,title
- genre=tech
- fields=id,title

## Schema

Xem schemas/book.json, author.json, review.json
