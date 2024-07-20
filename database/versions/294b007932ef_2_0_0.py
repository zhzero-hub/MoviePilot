"""2.0.0

Revision ID: 294b007932ef
Revises: 
Create Date: 2024-07-20 08:43:40.741251

"""

import random
import string

from app.core.config import settings
from app.core.security import get_password_hash
from app.db import SessionFactory
from app.db.models import *
from app.log import logger

# revision identifiers, used by Alembic.
revision = '294b007932ef'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """
    v2.0.0 数据库初始化
    """
    # 初始化超级管理员
    with SessionFactory() as db:
        _user = User.get_by_name(db=db, name=settings.SUPERUSER)
        if not _user:
            # 定义包含数字、大小写字母的字符集合
            characters = string.ascii_letters + string.digits
            # 生成随机密码
            random_password = ''.join(random.choice(characters) for _ in range(16))
            logger.info(
                f"【超级管理员初始密码】{random_password} 请登录系统后在设定中修改。 注：该密码只会显示一次，请注意保存。")
            _user = User(
                name=settings.SUPERUSER,
                hashed_password=get_password_hash(random_password),
                email="admin@movie-pilot.org",
                is_superuser=True,
            )
            _user.create(db)


def downgrade() -> None:
    pass
