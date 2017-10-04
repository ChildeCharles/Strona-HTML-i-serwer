# -*- coding: utf-8 -*-
import socket
import codecs
import mimetypes

HOST, PORT = '', 8808

mimetypes.add_type("image/svg+xml", ".svg", True)
mimetypes.add_type("image/svg+xml", ".svgz", True)

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
listen_socket.bind((HOST, PORT))
listen_socket.listen(1)
print 'Serving HTTP on port %s ...' % PORT
while True:
    print "LISTETNING..."
    client_connection, client_address = listen_socket.accept()
    request = client_connection.recv(1024)
    print request
    klucz = None
    wartosc = None
    filename = ""

    http_response = "HTTP/1.1 200 OK\n"

    request_lines = request.split('\n')
    for line in request_lines:
      if 'GET ' in line:		
        #print 'Prosba o zasob: %s' % (line)
        if '/logo1.png' in line:
	  filename = "www/logo1.png"
	if '/css/basic.css' in line:
	  filename = "www/css/basic.css"
	if '/image.svg' in line:
	  filename = "www/image.svg"
      elif 'HEAD ' in line:
        #print 'Prosba o zasob: %s' % (line)
        if '/logo1.png' in line:
          filename = "www/logo1.png"
        if '/css/basic.css' in line:
          filename = "www/css/basic.css"
        if '/image.svg' in line:
	  filename = "www/image.svg"
      else:
        #Headers
        podzielony_naglowek = line.split(':')
        if len(podzielony_naglowek) == 2:
          klucz, wartosc = line.split(':')
	  print '%s:%s' % (klucz, wartosc)
	  if "Accept-Language" in klucz:
            jezyk = wartosc[1:3]
	  if "Accept" in klucz and "Accept-" not in klucz:
	    accept = wartosc
    print ""
    print "Zaakceptowane:%s"%accept
    print "Jezyk: %s"%jezyk
    print ""
    if filename == "":
    #site selector
      if jezyk=="pl":
        if "text/plain" in accept:
          filename = "www/indexPL.txt"
	  content = "Content-Type: text/plain"
        elif "text/html" in accept:
          filename = "www/indexPL.html"
	  content = "Content-Type: text/html"
      elif jezyk=="en":
        if "text/plain" in accept:
          filename = "www/indexEN.txt"
	  content = "Content-Type: text/plain"
        elif "text/html" in accept:
          filename = "www/indexEN.html"
	  content = "Content-Type: text/html"
      else:
        filename = "www/indexEN.html"
	content = "Content-Type: text/html"
    #images and stylesheets loader
    elif ".svg" in filename and ("image/svg" in accept or "*/*" in accept):
      content = "Content-Type: image/svg+xml"
    elif ".css" in filename and ("text/css" in accept or "*/*" in accept):
      content = "Content-Type: text/css"
    elif ".png" in filename and ("image/png" in accept or "image/webp" or "*/*" in accept):
      content = "Content-Type: image/png"
    else:
      content = ""
      filename = ""
    #opening file if one is given
    if filename != "":
      try:
        plik = open(filename,"rb")    
        data = plik.read()
      except IOError:
        print"Nie znalazłem: %s"%filename
      finally:
        plik.close()
      Content_Lenght = str(len(data))
      http_response += content + "\n" + Content_Lenght + "\n\n" + data
  
    #http_response is 200 OK if no file is given.
    client_connection.sendall(http_response)
    client_connection.close()
