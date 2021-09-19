import logging
from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import PostImage


THUMBNAIL_SIZE = (300, 300)

logger = logging.getLogger(__name__)


@receiver(pre_save, sender=PostImage)
def generate_thumbnail(sender, instance, ** kwargs):
    logger.info('============== \n \n Generating thumbnail for post %d \n\n     ============= \n\n         Done! \n', instance.post.id)

    image = Image.open(instance.image)
    image = image.convert('RGB')
    image.thumbnail(THUMBNAIL_SIZE, Image.ANTIALIAS)
    temp_thumb = BytesIO()
    image.save(temp_thumb, 'png')
    temp_thumb.seek(0)

    # save=False, because otherwise it will run in an infinite loop!
    instance.thumbnail.save(instance.image.name, ContentFile(temp_thumb.read()), save=False)
    temp_thumb.close()