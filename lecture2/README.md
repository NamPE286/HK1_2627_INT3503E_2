(.venv) nambh@NamBH-MAC lecture2 % python -m unittest discover -s . -v       
test_create_book_returns_location_and_trims_text (test_app.BooksAPITestCase.test_create_book_returns_location_and_trims_text) ... ok
test_create_requires_non_blank_title_and_author (test_app.BooksAPITestCase.test_create_requires_non_blank_title_and_author) ... ok
test_delete_book_returns_204_and_removes_it (test_app.BooksAPITestCase.test_delete_book_returns_204_and_removes_it) ... ok
test_empty_collection_has_zero_total_pages (test_app.BooksAPITestCase.test_empty_collection_has_zero_total_pages) ... ok
test_filter_by_author_is_case_insensitive (test_app.BooksAPITestCase.test_filter_by_author_is_case_insensitive) ... ok
test_get_book_has_cache_header (test_app.BooksAPITestCase.test_get_book_has_cache_header) ... ok
test_ids_are_not_reused_after_deletion (test_app.BooksAPITestCase.test_ids_are_not_reused_after_deletion) ... ok
test_invalid_pagination_returns_400 (test_app.BooksAPITestCase.test_invalid_pagination_returns_400) ... ok
test_list_books_has_pagination_links_and_cache_header (test_app.BooksAPITestCase.test_list_books_has_pagination_links_and_cache_header) ... ok
test_list_books_paginates_and_exposes_navigation_links (test_app.BooksAPITestCase.test_list_books_paginates_and_exposes_navigation_links) ... ok
test_missing_book_returns_404_for_all_item_operations (test_app.BooksAPITestCase.test_missing_book_returns_404_for_all_item_operations) ... ok
test_pagination_values_are_bounded (test_app.BooksAPITestCase.test_pagination_values_are_bounded) ... ok
test_patch_rejects_negative_price_without_changing_book (test_app.BooksAPITestCase.test_patch_rejects_negative_price_without_changing_book) ... ok
test_patch_updates_only_supplied_fields (test_app.BooksAPITestCase.test_patch_updates_only_supplied_fields) ... ok
test_replace_book_requires_both_fields_and_replaces_resource (test_app.BooksAPITestCase.test_replace_book_requires_both_fields_and_replaces_resource) ... ok
test_search_title_is_case_insensitive_and_combines_with_author (test_app.BooksAPITestCase.test_search_title_is_case_insensitive_and_combines_with_author) ... ok

----------------------------------------------------------------------
Ran 16 tests in 0.021s

OK