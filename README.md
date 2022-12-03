# Installation

1. Move the NER model (`model-best`) folder inside `receipts_processing/ner-models/`

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

      Note: _If you have a Mac_ system you may not be able to install `paddleocr`. The reason for that is because it uses `PyMuPDF==1.19.0`, which can't be installed in Apple Silicon chips. To solve that, you need to clone the [`paddleocr`](https://github.com/PaddlePaddle/PaddleOCR) repo and override the version of PyMuPDF. To do that, follow these steps:

      1. Install PyMuPF dependencies using [brew](https://brew.sh/)

         ```bash
         brew install mupdf swig freetype
         ```

      2. Install PyMuPDF from source

         ```bash
         pip install https://github.com/pymupdf/PyMuPDF/archive/master.tar.gz
         ```

      3. Clone the [`paddleocr`](https://github.com/PaddlePaddle/PaddleOCR) repo
         ```bash
         git clone https://github.com/PaddlePaddle/PaddleOCR
         ```
      4. Open the repo with your editor, for example `code PaddleOCR`, then find every occurrence of `PyMuPDF==1.19.0` and replace it with `PyMuPDF==1.21.0`.

      5. Inside the `PaddleOCR` folder run

         ```bash
         pip install -r requirements.txt
         ```

         That will install all dependencies required for paddleocr.

      6. Install `paddlepaddle`

         ```bash
         pip install paddlepaddle
         ```

      7. Outside of `PaddleOCR` folder, install `paddleocr` from your local directory by running

         ```bash
         pip install ./PaddleOCR
         ```

         7. Execute general installation steps above.
3. Migrate the database:
   ```bash
   python manage.py migrate
   ```

# Usage

Open your terminal and `cd cpsc-4820-final-project`.

Then run:

```bash
python manage.py runserver
```

That should get Django started and you should be able to see the app running at http://localhost:8000

## Admin panel

We are using Django's built-in admin panel.

To create the admin user you need to run:

```bash
python manage.py createsuperuser
```

It will ask you to set an username, password and email. After you create the super user, you can log in at http://localhost:8000/admin