from django.shortcuts import render
from django.templatetags.static import static
from .forms import ContactForm
from .models import Contact
from django_ratelimit.decorators import ratelimit

def home(request):
    return render(request, 'core/home.html')

def about(request):
    social = {
  "x": static( 'social-logo/x.png' ),
  "ln": static( 'social-logo/ln.png' ),
  "ig": static( 'social-logo/ig.png' ),
  "yt": static( 'social-logo/yt.png' ),
  "fb": static( 'social-logo/fb.png' ),
}
    img=[ ]
    
    members = [
  {
    "name": "Pushkar Singh Kushwaha",
    "img": "",
    "role": "Lead Designer",
    "bio": "Specializes in blending traditional motifs with modern UI/UX principles.",
    "social": [
      {
        "link": "https://x.com/pushkar",
        "logo": social["x"]
      },
      {
        "link": "https://linkedin.com/in/pushkar",
        "logo": social["ln"]
      }
    ]
  },

  {
    "name": "AmanRaj Malhotra",
    "img": "",
    "role": "Full-Stack Developer",
    "bio": "Builds the technical foundation for cultural storytelling.",
    "social": [
      {
        "link": "https://youtube.com/@amanraj",
        "logo": social["yt"]
      },
      {
        "link": "https://facebook.com/amanraj",
        "logo": social["fb"]
      }
    ]
  },

  {
    "name": "Gautam Kushwaha",
    "img": static( 'core/images/gtm.jpg' ),
    "role": "Motivational speaker",
    "bio": "A JEE aspirant involved in high-tech web development. Motivating Millions! to achieve their goals.",
    "social": [
      {
        "link": "https://youtube.com/@gautam",
        "logo": social["yt"]
      },
      {
        "link": "https://x.com/gautam",
        "logo": social["x"]
      }
    ]
  },

  {
    "name": "Harshit Raj",
    "img": "",
    "role": "Proof Reader",
    "bio": "The truth of the page is due to him.",
    "social": [
      {
        "link": "https://linkedin.com/in/harshit",
        "logo": social["ln"]
      },
      {
        "link": "https://facebook.com/harshit",
        "logo": social["fb"]
      }
    ]
  },

  {
    "name": "Rajveer Pandey",
    "img": "",
    "role": "Content Writer",
    "bio": "Immerses the page into knowledge",
    "social": [
      {
        "link": "https://instagram.com/rajveer",
        "logo": social["ig"]
      },
      {
        "link": "https://x.com/rajveer",
        "logo": social["x"]
      }
    ]
  }
]

    return render(request, 'core/about.html',{'members':members})
@ratelimit(key="ip",rate="5/s", method='POST', block=True)
def contact(request):
    if request.method=='POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = ContactForm()
    return render(request, 'core/contact.html' ,{'form':form})


def services(request):
    return render(request, 'core/service.html')
