from django.db import models

# Let's create a proper Ad model so we can upload files easily in the django admin panel, and link them to NewsPosts via ForeignKey
class Ad(models.Model):
	company_name = models.CharField(max_length=200)
	copy = models.TextField(max_length=2000)
	logo = models.ImageField(max_length=200, upload_to='static/uploads/') # This required intstalling the Pillow module! But is useful over a FileField because it validates that the uploaded file is an image.
	url = models.URLField(max_length=200)
	house_ad = models.BooleanField(default=False)

	def __str__(self):
		return self.company_name