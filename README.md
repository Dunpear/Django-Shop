
# Verkana Shop

This is a simple e-commerce project developed using Django Rest Framework, with jQuery and Django used on the frontend.

The modules are implemented in a very simple and practical way..

This project is designed as a marketplace!

## Used By

This project is used by the following companies:

- DRF
- Django template
- Jquery


## packages

- drf_spectacular ( for schema )
- django jalali
- ckeditor
- colorfield
- corsheaders


## Installation

Before installation, you can create a virtual environment and put the project files inside it..



```bash
  pip install -r requirements.txt
```
    
## Usage/Examples

In the setting.py file of verkana_front, you can specify the api port and route by changing the base_url.

To use, you only need to start two projects with two different ports


```bash
server :
  py manage.py runserver 8000 

client:
  py manage.py runserver 3000
```


In the following you need create a superuser

```bash
  py manage.py createsuperuser
```

---

After that, we need to register the basic information in the database

path : http://127.0.0.1:8000/admin/

it's done :)
## Support

For any question, you can contact me via email
elvin.zeroday@gmail.com

good luck :)


