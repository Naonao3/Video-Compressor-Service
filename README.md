# Video-Compressor-Service
RecursionCSのBackendProject2_Video-Compressor-Serviceのリポジトリーになります。

## 概要
ユーザーが動画を圧縮し、異なるフォーマットや解像度に変換することができるクライアントサーバ分散アプリケーションです。</br>
クライアントのホストシステムの代わりにサーバのリソースを使用することで、ユーザーはどのようなプラットフォームやハードウェアからでもこれらの変換サービスを実行することができます。

## 実行方法
クライアントでは、ユーザーが自分のコンピュータからファイルを選択し、動画をアップロードしたり、選択したサービスに基づいて新しいバージョンの動画をダウンロードしたりできるようにします。


ユーザーに提供するサービスは以下の通りです。

- 動画ファイルを圧縮する: ユーザーは、サーバに動画ファイルをアップロードすると、そのファイルを小さく圧縮したものをダウンロードします。サーバは自動的に最適な圧縮方法を判断します。
- 動画の解像度を変更する: ユーザーは動画をアップロードし、使用したい解像度を選択すると、クライアントはこの新しい解像度の動画をダウンロードします。
- 動画の縦横比を変更する: ユーザーは動画をアップロードして、使用したい縦横比を選択し、クライアントはこの新しい動画をダウンロードします。
- 動画をオーディオに変換する: 動画ファイルをアップロードすると、その動画の音声のみを収録した MP3 バージョンがダウンロードされます。
- 時間範囲から GIF や WEBM を作成する: 動画をアップロードし、時間範囲を指定すると、サーバは動画をトリミングして GIF または WEBM に変換します。