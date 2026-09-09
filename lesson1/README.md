(.venv) nambh@NamBH-MAC kthdv % lesson1/.venv/bin/python -m unittest discover -s lesson1 -v
test_create_book_and_location (test_app.BooksAPITestCase.test_create_book_and_location) ... ok
test_create_requires_title_and_author (test_app.BooksAPITestCase.test_create_requires_title_and_author) ... ok
test_delete_has_empty_body_and_removes_book (test_app.BooksAPITestCase.test_delete_has_empty_body_and_removes_book) ... ok
test_get_book (test_app.BooksAPITestCase.test_get_book) ... ok
test_ids_are_not_reused_after_deletion (test_app.BooksAPITestCase.test_ids_are_not_reused_after_deletion) ... ok
test_invalid_limit (test_app.BooksAPITestCase.test_invalid_limit) ... ok
test_list_books (test_app.BooksAPITestCase.test_list_books) ... ok
test_list_empty_collection (test_app.BooksAPITestCase.test_list_empty_collection) ... ok
test_list_limit (test_app.BooksAPITestCase.test_list_limit) ... ok
test_missing_book (test_app.BooksAPITestCase.test_missing_book) ... ok
test_update_title_and_author (test_app.BooksAPITestCase.test_update_title_and_author) ... ok
test_update_title_preserves_other_fields (test_app.BooksAPITestCase.test_update_title_preserves_other_fields) ... ok

----------------------------------------------------------------------
Ran 12 tests in 0.008s

OK