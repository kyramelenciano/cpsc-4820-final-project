# Installation

1. Move the NER model (`model-best`) folder inside `receipts_processing/ner-models/`

2. Install required dependencies:
    ```
    pip install -r requirements.txt
    ```

Note: If you have a Mac system you may not be able to install `paddleocr`. The reason for that is because it uses `PyMuPDF==1.19.0`, which can't be installed in Apple Silicon chips. To solve that, you need to clone the [`paddleocr`](https://github.com/PaddlePaddle/PaddleOCR) repo and override the version of PyMuPDF. To do that, follow these steps:

1. Clone the repo
    ```
    git clone https://github.com/PaddlePaddle/PaddleOCR
    ```
2. Open the repo with your editor. For example `code PaddleOCR`.

3. Find every occurrence of `PyMuPDF==1.19.0` and replace it with `PyMuPDF-1.20.1`.

4. Install `paddleocr` from your local directory

    ```
    pip install ./PaddleOCR
    ```


# Usage

Open your terminal and `cd cpsc-4820-final-project`. 

Then run:

```
python manage.py runserver
```

That should get Django started and you should be able to see the app running at http://localhost:8000