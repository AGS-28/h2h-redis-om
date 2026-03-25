import sys
import shlex
from redis_om import Migrator
from app.models.base import redis
from app.models import MODEL_REGISTRY
from loguru import logger

def run_migrations():
    logger.info("🚀 Starting Redis OM migrations...")
    
    # Check for --force flag
    force = "--force" in sys.argv
    
    # Use MODEL_REGISTRY to automatically migrate all registered models
    # We use a set to avoid migrating the same class twice if there are aliases
    models = list(set(MODEL_REGISTRY.values()))
    
    for model in models:
        try:
            model_name = model.__name__
            meta = getattr(model, 'Meta', None)
            if not meta:
                continue
                
            global_prefix = getattr(meta, 'global_key_prefix', 'redis_om')
            model_prefix = getattr(meta, 'model_key_prefix', model_name.lower())
            index_name = f"{global_prefix}:{model_prefix}:index"
            
            logger.info(f"🛠️  Checking index for {model_name} ({index_name})...")
            
            if force:
                logger.warning(f"⚠️  Force mode: Dropping index '{index_name}'...")
                try:
                    redis.execute_command("FT.DROPINDEX", index_name)
                except Exception:
                    pass

            try:
                redis.execute_command("FT.INFO", index_name)
                logger.info(f"✅ Index '{index_name}' already exists.")
            except Exception:
                logger.info(f"📡 Creating index for {model_name} manually...")
                schema = model.redisearch_schema()
                cmd_parts = ["FT.CREATE", index_name] + shlex.split(schema)
                redis.execute_command(*cmd_parts)
                logger.info(f"✅ Index '{index_name}' created successfully!")
                
        except Exception as e:
            logger.error(f"❌ Failed to migrate {model_name}: {e}")

    try:
        logger.info("🔃 Running general Migrator for any other tasks...")
        Migrator().run()
        logger.info("✅ All migrations completed successfully!")
    except Exception as e:
        logger.warning(f"⚠️  Migrator notice: {e}")

if __name__ == "__main__":
    run_migrations()
