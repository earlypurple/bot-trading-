from playwright.sync_api import sync_playwright, Page, expect

def run_verification():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        try:
            # Navigate to the page
            page.goto("http://localhost:5000")

            # Wait for a key element to be visible
            expect(page.get_by_role("heading", name="Tableau de Bord")).to_be_visible()

            # Take a screenshot
            page.screenshot(path="jules-scratch/verification/dashboard.png")

            print("Screenshot taken successfully.")

        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    run_verification()
