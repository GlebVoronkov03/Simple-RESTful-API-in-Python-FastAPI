from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status

from ..auth.auth_config import current_user
from ..config import settings
from .tasks import send_email

router = APIRouter()


@router.get("/report")
def send_report(background_tasks: BackgroundTasks,
                user=Depends(current_user)):
    try:
        sending_data = {
            'email': user.email,
            'subject': 'Заказанная картинка',
            'massage': (
                '<div>'
                f'<h1>Здравствуйте, {user.full_name}, ваша картинка.</h1>'
                '<img src="https://img5.goodfon.ru/original/1920x1080/2/'
                '18/portret-devushki-so-spiny-ruki-za-golovoi-v-temnote.jpg"'
                ' width="600">'
                '</div>'
            )
        }
        if settings.is_tests:
            background_tasks.add_task(send_email, sending_data)
        else:
            send_email.delay(sending_data)
        return {
            "status": status.HTTP_200_OK,
            "data": "Письмо отправлено",
            "details": None
        }
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "status": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "data": None,
                "details": str(error),
            },
        )
