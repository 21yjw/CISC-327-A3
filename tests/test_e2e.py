import pytest
from playwright.sync_api import Page, expect


#test if navigating to page works
def test_open_catalog(page: Page, live_server_url):
    page.goto(f"{live_server_url}")
    
    expect(page).to_have_title("Library Management System")
    expect(page).to_have_url(f"{live_server_url}/catalog")

#test navigating between different sections
def test_navigate_page(page: Page, live_server_url):
    page.goto(f"{live_server_url}")
    
    #navigate to catalog
    page.click("text=📖 Catalog")
    page.wait_for_load_state("networkidle")
    
    expect(page).to_have_title("Library Management System")
    expect(page).to_have_url(f"{live_server_url}/catalog")
    h2 = page.locator("body > div.content > h2")
    expect(h2).to_be_visible()
    expect(h2).to_have_text("📖 Book Catalog")
    
    #navigate to add book
    page.click("text=➕ Add Book")
    page.wait_for_load_state("networkidle")
    
    expect(page).to_have_title("Library Management System")
    expect(page).to_have_url(f"{live_server_url}/add_book")
    h2 = page.locator("body > div.content > h2")
    expect(h2).to_be_visible()
    expect(h2).to_have_text("➕ Add New Book")
    
    #navigate to return book
    page.click("text=↩️ Return Book")
    page.wait_for_load_state("networkidle")
    
    expect(page).to_have_title("Library Management System")
    expect(page).to_have_url(f"{live_server_url}/return")
    h2 = page.locator("body > div.content > h2")
    expect(h2).to_be_visible()
    expect(h2).to_have_text("↩️ Return Book")
    
    #navigate to search
    page.click("text=🔍 Search")
    page.wait_for_load_state("networkidle")
    
    expect(page).to_have_title("Library Management System")
    expect(page).to_have_url(f"{live_server_url}/search")
    h2 = page.locator("body > div.content > h2")
    expect(h2).to_be_visible()
    expect(h2).to_have_text("🔍 Search Books")

#test catalog elements
def test_catalog_elements(page: Page, live_server_url):
    page.goto(f"{live_server_url}/catalog")

    #check main header and paragraph
    expect(page.locator("body > div.content > h2")).to_have_text("📖 Book Catalog")
    expect(page.locator("body > div.content > p")).to_have_text("Browse all available books in our library collection.")

    #check table headers
    headers = page.locator("body > div.content > table > thead > tr > th")
    expected_headers = ["ID", "Title", "Author", "ISBN", "Availability", "Actions"]
    assert headers.count() == len(expected_headers)
    for i, text in enumerate(expected_headers):
        expect(headers.nth(i)).to_have_text(text)

    #check at least one book row exists
    rows = page.locator("body > div.content > table > tbody > tr")
    count = rows.count()
    assert count > 0

    #check first row cells
    first_row = rows.first
    cells = first_row.locator("td")
    assert cells.count() == 6

#test add book elements
def test_add__book_elements(page: Page, live_server_url):
    page.goto(f"{live_server_url}/add_book")

    #check main header
    expect(page.locator("body > div.content > h2")).to_have_text("➕ Add New Book")

    #check description paragraph
    expect(page.locator("body > div.content > p")).to_have_text("Add a new book to the library catalog.")

    #check form
    form = page.locator("body > div.content > form")
    form_action = form.get_attribute("action")
    assert form_action == "/add_book"

    #title
    title_label = page.locator("label[for='title']")
    expect(title_label).to_have_text("Title *")

    title_input = page.locator("input#title")
    expect(title_input).to_have_attribute("maxlength", "200")
    expect(title_input).to_have_attribute("required", "")
    expect(title_input).to_have_attribute("name", "title")

    title_note = page.locator("input#title + small")
    expect(title_note).to_have_text("Maximum 200 characters")

    #author
    author_label = page.locator("label[for='author']")
    expect(author_label).to_have_text("Author *")

    author_input = page.locator("input#author")
    expect(author_input).to_have_attribute("maxlength", "100")
    expect(author_input).to_have_attribute("required", "")
    expect(author_input).to_have_attribute("name", "author")

    author_note = page.locator("input#author + small")
    expect(author_note).to_have_text("Maximum 100 characters")

    #ISBN
    isbn_label = page.locator("label[for='isbn']")
    expect(isbn_label).to_have_text("ISBN *")

    isbn_input = page.locator("input#isbn")
    expect(isbn_input).to_have_attribute("maxlength", "13")
    expect(isbn_input).to_have_attribute("required", "")
    expect(isbn_input).to_have_attribute("name", "isbn")

    isbn_note = page.locator("input#isbn + small")
    expect(isbn_note).to_have_text("Exactly 13 digits (e.g., 9780743273565)")

    #total copies
    copies_label = page.locator("label[for='total_copies']")
    expect(copies_label).to_have_text("Total Copies *")

    copies_input = page.locator("input#total_copies")
    expect(copies_input).to_have_attribute("min", "1")
    expect(copies_input).to_have_attribute("required", "")
    expect(copies_input).to_have_attribute("name", "total_copies")

    copies_note = page.locator("input#total_copies + small")
    expect(copies_note).to_have_text("Must be a positive integer")

    #submit button and cancel button
    submit_btn = page.locator("button[type='submit']")
    expect(submit_btn).to_have_text("Add Book to Catalog")
    expect(submit_btn).to_have_class("btn btn-success")

    cancel_link = page.locator("a.btn", has_text="Cancel")
    expect(cancel_link).to_be_visible()

    #validation rules box
    validation_box = page.locator("div[style*='background-color']")
    expect(validation_box.locator("h4")).to_have_text("📝 Validation Rules:")

    validation_list_items = validation_box.locator("ul li")
    expected_validation_texts = [
        "Title: Required, maximum 200 characters",
        "Author: Required, maximum 100 characters",
        "ISBN: Required, exactly 13 digits, must be unique",
        "Total Copies: Required, positive integer",
    ]
    assert validation_list_items.count() == len(expected_validation_texts)

    for i, text in enumerate(expected_validation_texts):
        expect(validation_list_items.nth(i)).to_contain_text(text)

#test return book elements
def test_return_book_elements(page: Page, live_server_url):
    page.goto(f"{live_server_url}/return")

    #check heading and description paragraph
    expect(page.locator("body > div.content > h2")).to_have_text("↩️ Return Book")
    expect(page.locator("body > div.content > p")).to_have_text("Return a borrowed book to the library.")

    #check form and its action attribute (should not literally contain 'borrowing.return_book')
    form = page.locator("body > div.content > form")
    form_action = form.get_attribute("action")
    assert form_action == "/return"

    #patron ID
    patron_label = page.locator("label[for='patron_id']")
    expect(patron_label).to_have_text("Patron ID *")

    patron_input = page.locator("input#patron_id")
    expect(patron_input).to_have_attribute("name", "patron_id")
    expect(patron_input).to_have_attribute("pattern", "[0-9]{6}")
    expect(patron_input).to_have_attribute("maxlength", "6")
    expect(patron_input).to_have_attribute("required", "")

    patron_note = page.locator("input#patron_id + small")
    expect(patron_note).to_have_text("6-digit library card number")

    #book ID
    book_label = page.locator("label[for='book_id']")
    expect(book_label).to_have_text("Book ID *")

    book_input = page.locator("input#book_id")
    expect(book_input).to_have_attribute("name", "book_id")
    expect(book_input).to_have_attribute("min", "1")
    expect(book_input).to_have_attribute("required", "")

    book_note = page.locator("input#book_id + small")
    expect(book_note).to_have_text("The ID of the book you want to return")

    #submit button
    submit_btn = page.locator("button[type='submit']")
    expect(submit_btn).to_have_text("Process Return")
    expect(submit_btn).to_have_class("btn btn-success")

    #cancel button
    cancel_link = page.locator("a.btn", has_text="Cancel")
    expect(cancel_link).to_be_visible()

#test search bar elements
def test_search__elements(page: Page, live_server_url):
    page.goto(f"{live_server_url}/search")

    #check heading and description paragraph
    expect(page.locator("body > div.content > h2")).to_have_text("🔍 Search Books")
    expect(page.locator("body > div.content > p")).to_have_text("Find books in the library catalog.")

    #check search input
    search_input = page.locator("input#q")
    expect(search_input).to_be_visible()
    expect(search_input).to_have_attribute("name", "q")
    expect(search_input).to_have_attribute("required", "")

    search_note = page.locator("input#q + small")
    expect(search_note).to_have_text("Enter title, author, or ISBN to search")

    #check search type select and options
    select = page.locator("select#type")
    expect(select).to_be_visible()
    expect(select).to_have_attribute("name", "type")

    options = select.locator("option")
    expected_options = [
        ("title", "Title (partial match)"),
        ("author", "Author (partial match)"),
        ("isbn", "ISBN (exact match)"),
    ]
    assert options.count() == len(expected_options)
    for i, (value, text) in enumerate(expected_options):
        expect(options.nth(i)).to_have_attribute("value", value)
        expect(options.nth(i)).to_have_text(text)

    #check buttons
    submit_btn = page.locator("button[type='submit']")
    expect(submit_btn).to_have_text("🔍 Search")
    expect(submit_btn).to_have_class("btn")

    view_all_link = page.locator("a.btn", has_text="View All Books")
    expect(view_all_link).to_be_visible()

#test workflow add book and check and search for book
def test_workflow1(page: Page, live_server_url):
    page.goto(f"{live_server_url}")
    
    BOOK_TITLE = "BOOK NAME"
    BOOK_AUTHOR = "AUTHOR NAME"
    BOOK_ISBN = "1234567890123"
    BOOK_COPIES = "5"
    
    
    #navigate to add book
    page.click("text=➕ Add Book")
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url(f"{live_server_url}/add_book")
    
    #enter details
    page.fill("input#title", BOOK_TITLE)
    page.fill("input#author", BOOK_AUTHOR)
    page.fill("input#isbn", BOOK_ISBN)
    page.fill("input#total_copies", BOOK_COPIES)
    
    #submit details
    page.click("body > div.content > form > div:nth-child(5) > button.btn-success")
    page.wait_for_load_state("networkidle")
    
    #go to catalog
    page.click("text=📖 Catalog")
    page.wait_for_load_state("networkidle")
    
    #check for book
    rows = page.locator("body > div.content > table > tbody > tr")
    found = False
    for i in range(rows.count()):
        row = rows.nth(i)
        title_cell = row.locator("td").nth(1)
        title_text = title_cell.inner_text().strip()
        author_cell = row.locator("td").nth(2)
        author_text = author_cell.inner_text().strip()
        isbn_cell = row.locator("td").nth(3)
        isbn_text = isbn_cell.inner_text().strip()
        print(title_text, author_text, isbn_text);
        if title_text == BOOK_TITLE and author_text == BOOK_AUTHOR and isbn_text == BOOK_ISBN:
            found = True
            break

    assert found
    
    #navigate to search
    page.click("text=🔍 Search")
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url(f"{live_server_url}/search")
    
    #search
    page.fill("input#q", BOOK_TITLE)
    page.click("body > div.content > form > div:nth-child(3) > button")
    page.wait_for_load_state("networkidle")
    
    #check for book
    rows = page.locator("body > div.content > table > tbody > tr")
    found = False
    for i in range(rows.count()):
        row = rows.nth(i)
        title_cell = row.locator("td").nth(1)
        title_text = title_cell.inner_text().strip()
        author_cell = row.locator("td").nth(2)
        author_text = author_cell.inner_text().strip()
        isbn_cell = row.locator("td").nth(3)
        isbn_text = isbn_cell.inner_text().strip()
        print(title_text, author_text, isbn_text);
        if title_text == BOOK_TITLE and author_text == BOOK_AUTHOR and isbn_text == BOOK_ISBN:
            found = True
            break
    
    assert found

#test workflow add borrow return book
def test_workflow2(page: Page, live_server_url):
    page.goto(f"{live_server_url}")
    
    BOOK_TITLE = "BOOK NAME2"
    BOOK_AUTHOR = "AUTHOR NAME2"
    BOOK_ISBN = "1234567890124"
    BOOK_COPIES = "3"
    BOOK_ID = None
    PATRON_ID = "123456"
    
    
    #navigate to add book
    page.click("text=➕ Add Book")
    page.wait_for_load_state("networkidle")
    expect(page).to_have_url(f"{live_server_url}/add_book")
    
    #enter details
    page.fill("input#title", BOOK_TITLE)
    page.fill("input#author", BOOK_AUTHOR)
    page.fill("input#isbn", BOOK_ISBN)
    page.fill("input#total_copies", BOOK_COPIES)
    
    #submit details
    page.click("body > div.content > form > div:nth-child(5) > button.btn-success")
    page.wait_for_load_state("networkidle")
    
    #go to catalog
    page.click("text=📖 Catalog")
    page.wait_for_load_state("networkidle")
    
    #find book and borrow
    rows = page.locator("body > div.content > table > tbody > tr")
    found = False
    for i in range(rows.count()):
        row = rows.nth(i)
        title_cell = row.locator("td").nth(1)
        title_text = title_cell.inner_text().strip()
        author_cell = row.locator("td").nth(2)
        author_text = author_cell.inner_text().strip()
        isbn_cell = row.locator("td").nth(3)
        isbn_text = isbn_cell.inner_text().strip()
        print(title_text, author_text, isbn_text);
        if title_text == BOOK_TITLE and author_text == BOOK_AUTHOR and isbn_text == BOOK_ISBN:
            found = True
            
            available = row.locator("td").nth(4).locator("span")
            available_text = available.inner_text().strip()
            assert available_text == f"{BOOK_COPIES}/{BOOK_COPIES} Available"
            
            id_cell = row.locator("td").nth(0)
            id_text = id_cell.inner_text().strip()
            BOOK_ID = id_text
            
            #enter patron id
            actions = row.locator("td").nth(5)
            actions.locator("form > input[type=text]:nth-child(2)").fill(PATRON_ID)
            actions.locator("form > button.btn-success").click()
            page.wait_for_load_state("networkidle")
            
            #check amount lowered
            available_text = available.inner_text().strip()
            assert available_text == f"{int(BOOK_COPIES)-1}/{BOOK_COPIES} Available"
            
            break
    
    assert found
    
    #navigate to return tab
    page.click("text=↩️ Return Book")
    page.wait_for_load_state("networkidle")
    
    #fill data
    page.fill("#patron_id", PATRON_ID)
    page.fill("#book_id", BOOK_ID)
    
    #borrow book
    page.click("body > div.content > form > div:nth-child(3) > button.btn-success")
    page.wait_for_load_state("networkidle")
    
    #navigate to catalog tab
    page.click("text=📖 Catalog")
    page.wait_for_load_state("networkidle")
    
    #check amount correct
    rows = page.locator("body > div.content > table > tbody > tr")
    found = False
    for i in range(rows.count()):
        row = rows.nth(i)
        title_cell = row.locator("td").nth(1)
        title_text = title_cell.inner_text().strip()
        author_cell = row.locator("td").nth(2)
        author_text = author_cell.inner_text().strip()
        isbn_cell = row.locator("td").nth(3)
        isbn_text = isbn_cell.inner_text().strip()
        print(title_text, author_text, isbn_text);
        if title_text == BOOK_TITLE and author_text == BOOK_AUTHOR and isbn_text == BOOK_ISBN:
            found = True
            
            available = row.locator("td").nth(4).locator("span")
            available_text = available.inner_text().strip()
            assert available_text == f"{BOOK_COPIES}/{BOOK_COPIES} Available"
            
            break
    
    assert found







