# from django.test import TestCase
# from django.core.files.images import ImageFile
# from posts import models


# class TestSignal(TestCase):
#     def test_thumbnails_are_generated_on_save(self):
#         post = models.Post(
#             content = 'Hey there this test post 1'
#         )
#         post.save()
#         with open(
#                 'posts/fixtures/test-post-image-1.jpg', 'rb') as f:
#             image = models.PostImage(
#                 post=post,
#                 image=ImageFile(f, name='tpi1.jpg')
#             )
#             with self.assertLogs('posts', level='INFO') as cm:
#                 image.save()

#         self.assertGreaterEqual(len(cm.output), 1)
#         image.refresh_from_db()

#         with open(
#             'posts/fixtures/test-post-image-1.jpg', 'rb') as f:   
#             expected_content = f.read()
#             assert image.thumbnail.read() == expected_content

#         image.thumbnail.delete(save=False)
#         image.image.delete(save=False)
