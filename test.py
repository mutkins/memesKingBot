from db.users import get_user_from_db_by_chat_id
from tools import extract_user_fullname
from tasks.inauguration import do_inauguration
from db.messages import get_id_user_has_the_most_likes

user = get_id_user_has_the_most_likes(chat_id='-1001945334192')
print()