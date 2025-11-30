from typing import Optional
import logging
import time

from src.agents.digest import DigestAgent
from src.database.repository import Repository

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Gemini Free Tier: 10 requests per minute
# 60 seconds / 10 = 6 seconds per request minimum
# Use 7 seconds to be safe
RATE_LIMIT_DELAY = 7  # seconds between API calls


def process_digests(limit: Optional[int] = None) -> dict:
    agent = DigestAgent()
    repo = Repository()

    articles = repo.get_articles_without_digest(limit=limit)
    total = len(articles)
    processed = 0
    failed = 0

    logger.info(f"Starting digest processing for {total} articles")

    for idx, article in enumerate(articles, 1):
        article_type = article["type"]
        article_id = article["id"]
        article_title = article["title"][:60] + "..." if len(article["title"]) > 60 else article["title"]

        logger.info(f"[{idx}/{total}] Processing {article_type}: {article_title} (ID: {article_id})")

        try:
            # Generate digest with retry logic for rate limits
            max_retries = 3
            retry_count = 0
            digest_result = None

            while retry_count < max_retries:
                try:
                    digest_result = agent.generate_digest(
                        title=article["title"],
                        content=article["content"],
                        article_type=article_type
                    )
                    break  # Success, exit retry loop

                except Exception as e:
                    error_msg = str(e)
                    if "429" in error_msg or "RESOURCE_EXHAUSTED" in error_msg:
                        retry_count += 1
                        if retry_count < max_retries:
                            wait_time = 15 * retry_count  # 15s, 30s, 45s
                            logger.warning(f"[RATE LIMIT] Retry {retry_count}/{max_retries} after {wait_time}s...")
                            time.sleep(wait_time)
                        else:
                            logger.error(f"[RATE LIMIT] Max retries reached for {article_id}")
                            raise
                    else:
                        raise  # Non-rate-limit error, fail immediately

            if digest_result:
                repo.create_digest(
                    article_type=article_type,
                    article_id=article_id,
                    url=article["url"],
                    title=digest_result.title,
                    summary=digest_result.summary,
                    published_at=article.get("published_at")
                )
                processed += 1
                logger.info(f"[OK] Successfully created digest for {article_type} {article_id}")

                # Rate limit: Wait before next request (except for last article)
                if idx < total:
                    logger.info(f"⏱️  Waiting {RATE_LIMIT_DELAY}s (rate limit)...")
                    time.sleep(RATE_LIMIT_DELAY)
            else:
                failed += 1
                logger.warning(f"[FAIL] Failed to generate digest for {article_type} {article_id}")

        except Exception as e:
            failed += 1
            logger.error(f"[ERROR] Error processing {article_type} {article_id}: {e}")

    logger.info(f"Processing complete: {processed} processed, {failed} failed out of {total} total")

    return {
        "total": total,
        "processed": processed,
        "failed": failed
    }


if __name__ == "__main__":
    result = process_digests()
    print(f"Total articles: {result['total']}")
    print(f"Processed: {result['processed']}")
    print(f"Failed: {result['failed']}")
