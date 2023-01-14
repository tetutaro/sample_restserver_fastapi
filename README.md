# sample_restserver_fastapi

A sample REST server using FastAPI

## 工夫した点

* バージョン番号の一元的な管理
    * https://packaging.python.org/en/latest/guides/single-sourcing-package-version/#single-sourcing-the-package-version
    * poetry-dynamic-versioning を使う
    * https://github.com/mtkennerly/poetry-dynamic-versioning
* FastAPI が Listen するポート番号を 8930 にした
    * 8000, 8080, 8888 などは使いたくない
    * でも 8000 番台以外にすると何故か Swagger UI が表示されない
* CORS を回避するための設定
    * backend/api.py で CORSMiddleware を使う
* FastAPI のログを uvicorn と一緒に流す
    * backend/api.py で `getLogger("uvicorn")` とする
* Swagger UI の URL を変更する
    * FastAPI の引数で一旦無効にし、`get_swagger_ui_html()` を使う
* Swagger UI で API を種別毎に表示する
    * `tags_metadata` の作成と API 毎の tag の設定
* Exception が raise された時に、直接 error response を返す
    * `exception_handler` の設定
* Swagger UI でエラーも詳細に表示する
    * backend/api.py で `error_response` の作成と、各 API で responses の設定
* favicon の表示
    * StaticFiles の設定と、FileResponse の設定
* pydantic で validate function の共有
    * `validator()` の中で `allow_reuse` の設定
* sphinx で必要な設定を pyproject.toml に集約する
    * [sphinx-pyproject-poetry](https://github.com/tetutaro/sphinx-pyproject-poetry.git) の利用
* gunicorn の logger の名前を変え、使いやすいようにする
    * gunicorn.logging.conf の設定
* gunicorn の access log のフォーマットを一般的なログに合わせて見やすいようにする
    * gunicorn.logging.conf の設定
