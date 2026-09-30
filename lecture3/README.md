# Blog API routes

Tiền tố `/api/v1`

```text
/posts                              GET, POST
/posts/{post_id}                    GET, PUT, PATCH, DELETE
/posts/{post_id}/comments           GET, POST
/posts/{post_id}/comments/{comment_id} GET, PATCH, DELETE
/posts/{post_id}/tags               GET
/posts/{post_id}/tags/{tag_id}      PUT, DELETE
/tags                               GET, POST
/tags/{tag_id}                      GET, PATCH, DELETE
/users                              GET, POST
/users/{user_id}                    GET, PATCH
/users/{user_id}/posts              GET
/users/{user_id}/following          GET
/users/{user_id}/following/{target_id} PUT, DELETE
/users/{user_id}/followers          GET
```

`posts`, `tags` và `users` là các collection; URI có ID là item. Bình luận nằm dưới bài viết, còn tag có collection riêng vì một thẻ dùng được cho nhiều bài. `following` biểu diễn quan hệ theo dõi; `followers` là chiều ngược lại
