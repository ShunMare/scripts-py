import requests
from requests.auth import HTTPBasicAuth
from src.log_operations.log_handlers import setup_logger

logger = setup_logger(__name__)


class WordPressAPI:
    def __init__(self, url, username, app_password):
        """
        WordPressAPIクラスの初期化
        :param url: WordPressサイトのURL
        :param username: ユーザー名
        :param app_password: アプリケーションパスワード
        """
        self.base_url = f"{url}/wp-json/wp/v2"
        self.auth = HTTPBasicAuth(username, app_password)
        logger.info(f"WordPress API initialized for {url}")

    def create_post(
        self,
        title,
        content,
        status="draft",
        categories=None,
        tags=None,
        meta_description=None,
        meta_keywords=None,
        seo_title=None,
        permalink=None,
    ):
        """
        新しい投稿を作成する
        :param title: 投稿のタイトル
        :param content: 投稿の内容
        :param status: 投稿のステータス（デフォルトは"draft"）
        :param categories: カテゴリーのリスト
        :param tags: タグのリスト
        :param meta_description: メタディスクリプション
        :param meta_keywords: メタキーワード
        :param seo_title: SEOタイトル
        :param permalink: カスタムパーマリンク
        :return: 作成された投稿のID、失敗した場合はNone
        """
        endpoint = f"{self.base_url}/posts"
        data = {
            "title": title,
            "content": content,
            "status": status,
        }

        logger.debug(f"Creating post with title: {title}")

        if categories:
            category_ids = self.get_category_ids(categories)
            data["categories"] = category_ids

        if tags:
            tag_ids = self.get_tag_ids(tags)
            data["tags"] = tag_ids

        # Cocoon用のメタデータ設定
        if meta_description is not None:
            data["the_page_meta_description"] = meta_description
        if meta_keywords is not None:
            data["the_page_meta_keywords"] = meta_keywords
        if seo_title is not None:
            data["the_page_seo_title"] = seo_title

        # パーマリンクの設定
        if permalink:
            data["slug"] = permalink

        try:
            response = requests.post(endpoint, json=data, auth=self.auth)
            response.raise_for_status()
            post_id = response.json().get("id")
            logger.info(f"Post created successfully. Post ID: {post_id}")
            return post_id
        except requests.RequestException as e:
            logger.error(f"Failed to create post: {str(e)}")
            return None

    def update_post(
        self,
        post_id,
        title=None,
        content=None,
        status=None,
        meta_description=None,
        meta_keywords=None,
        seo_title=None,
        permalink=None,
    ):
        """
        既存の投稿を更新する
        :param post_id: 更新する投稿のID
        :param title: 新しいタイトル（オプション）
        :param content: 新しい内容（オプション）
        :param status: 新しいステータス（オプション）
        :param meta_description: 新しいメタディスクリプション（オプション）
        :param meta_keywords: 新しいメタキーワード（オプション）
        :param seo_title: 新しいSEOタイトル（オプション）
        :param permalink: 新しいパーマリンク（オプション）
        :return: 更新が成功した場合はTrue、失敗した場合はFalse
        """
        endpoint = f"{self.base_url}/posts/{post_id}"
        data = {}
        if title:
            data["title"] = title
        if content:
            data["content"] = content
        if status:
            data["status"] = status

        logger.debug(f"Updating post {post_id}")

        # メタデータの更新
        meta = {}
        if meta_description is not None:
            meta["the_page_meta_description"] = meta_description
        if meta_keywords is not None:
            meta["the_page_meta_keywords"] = meta_keywords
        if seo_title is not None:
            meta["the_page_seo_title"] = seo_title

        if meta:
            data["meta"] = meta

        # パーマリンクの更新
        if permalink:
            data["slug"] = permalink

        try:
            response = requests.post(endpoint, json=data, auth=self.auth)
            response.raise_for_status()
            logger.info(f"Post {post_id} updated successfully")
            return True
        except requests.RequestException as e:
            logger.error(f"Failed to update post {post_id}: {str(e)}")
            return False

    def get_post(self, post_id):
        """
        指定されたIDの投稿を取得する
        :param post_id: 取得する投稿のID
        :return: 投稿データ、取得に失敗した場合はNone
        """
        endpoint = f"{self.base_url}/posts/{post_id}?_embed"
        try:
            logger.debug(f"Retrieving post {post_id}")
            response = requests.get(endpoint, auth=self.auth)
            response.raise_for_status()
            post = response.json()
            logger.info(f"Retrieved post {post_id}")
            logger.debug(f"Get post response: {post}")
            return post
        except requests.RequestException as e:
            logger.error(f"Failed to retrieve post {post_id}: {str(e)}")
            return None

    def get_category_ids(self, category_names):
        """
        指定されたカテゴリー名に対応するIDを取得する
        :param category_names: カテゴリー名のリスト
        :return: カテゴリーIDのリスト
        """
        endpoint = f"{self.base_url}/categories"
        category_ids = []
        for name in category_names:
            try:
                logger.debug(f"Retrieving category ID for '{name}'")
                response = requests.get(
                    endpoint, params={"search": name}, auth=self.auth
                )
                response.raise_for_status()
                categories = response.json()
                if categories:
                    category_ids.append(categories[0]["id"])
                    logger.info(f"Category '{name}' found. ID: {categories[0]['id']}")
                else:
                    logger.warning(f"Category '{name}' not found")
            except requests.RequestException as e:
                logger.error(f"Failed to retrieve category '{name}': {str(e)}")
        return category_ids

    def get_tag_ids(self, tag_names):
        """
        指定されたタグ名に対応するIDを取得する
        :param tag_names: タグ名のリスト
        :return: タグIDのリスト
        """
        endpoint = f"{self.base_url}/tags"
        tag_ids = []
        for name in tag_names:
            try:
                logger.debug(f"Retrieving tag ID for '{name}'")
                response = requests.get(
                    endpoint, params={"search": name}, auth=self.auth
                )
                response.raise_for_status()
                tags = response.json()
                if tags:
                    tag_ids.append(tags[0]["id"])
                    logger.info(f"Tag '{name}' found. ID: {tags[0]['id']}")
                else:
                    logger.warning(f"Tag '{name}' not found")
            except requests.RequestException as e:
                logger.error(f"Failed to retrieve tag '{name}': {str(e)}")
        return tag_ids

    def print_post_details(self, post):
        """
        投稿の詳細情報をログに出力する
        :param post: 投稿データ
        """
        logger.info(f"Post ID: {post['id']}")
        logger.info(f"Title: {post['title']['rendered']}")
        logger.info(f"Slug: {post['slug']}")
        logger.info(
            f"Meta Description: {post['meta'].get('the_page_meta_description', [''])[0] if 'meta' in post else 'Not set'}"
        )
        logger.info(
            f"Meta Keywords: {post['meta'].get('the_page_meta_keywords', [''])[0] if 'meta' in post else 'Not set'}"
        )
        logger.info(
            f"SEO Title: {post['meta'].get('the_page_seo_title', [''])[0] if 'meta' in post else 'Not set'}"
        )
