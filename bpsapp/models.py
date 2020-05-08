from django.contrib.auth.models import User, Group
from django.db import models

class Timestamp(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class City(Timestamp):
    name = models.CharField(max_length=200)
    district = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class LocationCategory(Timestamp):
    title = models.CharField(max_length=50)
    image = models.ImageField(upload_to="locationcategory")

    def __str__(self):
        return self.title

class LocationGuider(Timestamp):
	name=models.CharField(max_length=50)
	mobile=models.CharField(max_length=20)

	def __str__(self):
		return self.name


class Location(Timestamp):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to="location")
    category = models.ManyToManyField(LocationCategory)
    locationguider=models.ForeignKey(LocationGuider, on_delete=models.CASCADE)
    # tags = models.ManyToManyField(Tag)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    description = models.TextField()
    view_count = models.BigIntegerField(default=0)

    def __str__(self):
        return self.title



class Blog(Timestamp):
    
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to="blogs")
   

    def __str__(self):
        return self.title



class Visitor(Timestamp):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    mobile = models.CharField(max_length=50)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200, null=True, blank=True)
    photo = models.ImageField(upload_to='visitors', null=True, blank=True)
    interests = models.ManyToManyField(LocationCategory)


    def save(self, *args, **kwargs):
        grp, created = Group.objects.get_or_create(name='visitor')
        self.user.groups.add(grp)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
        
Rating = (
    ("Excellent", "Excellent"),
    ("Good", "Good"),
    ("Average", "Average"),
    ("Poor", "Poor"),
    ("Not Good", "Not Good"),

)

class LocationReview(Timestamp):
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    commenter = models.ForeignKey(Visitor, on_delete=models.CASCADE)
    review = models.TextField()
    rating = models.CharField(max_length=50, choices=Rating)


class Siteinformation(Timestamp):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='siteinformation')
    about = models.TextField()

    def __str__(self):
        return self.title

class Reply(Timestamp):
    text=models.TextField()
    review = models.ForeignKey(LocationReview, on_delete=models.CASCADE, null=True,blank=True)
    date=models.DateTimeField(auto_now_add=True)

      

