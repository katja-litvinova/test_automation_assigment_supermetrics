This is UI and API tests for Supermetrics Kitty Manager.


# Running the test app
This is a relatively simple Next.js app written in TypeScript. The app located in
~/test_automation_assignment_supermetrics/application

To run it you should,
1. Install dependencies with yarn
2. Start the dev server with yarn dev

# Instruction for using:

1. Install python 3.9
2. Install pip 21.1.2
3. Create and activate a virtual environment
4. Install the necessary environment requirements (libraries, modules, packages etc.):

    ```bash
    pip install -r requirements.txt
    ```

5. Download [Chromedriver](https://chromedriver.chromium.org/downloads), place it in venv/bin
6. Run tests:

   API tests:
   ```bash
    python -m pytest tests/test_api.py 
    ```
   UI tests:
   ```bash
     python -m pytest tests/test_ui.py
    ```
