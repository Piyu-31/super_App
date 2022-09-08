# nexussuperapp



For ssl handshake follow the below steps:  
pip install pymongo[srv]  

pip install pymongo[tls]  
pip install certifi  


add this in code(db page)  
import certifi  
ca = certifi.where()  
tlsCAFile = ca  
