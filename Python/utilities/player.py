import imp
from webbrowser import get
from utilities.music import music
import pygame
from utilities.dialoghi import dialogo
from utilities.collisioni import collisioni

class player():
   def __init__(self, immaginiP, OFFSET_FINESTRA,x,y,FPS,speed,walkcount):
      self.img=immaginiP["kikiF0"]
      self.walkleft=[
            immaginiP["kikiS0"],immaginiP["kikiS1"],immaginiP["kikiS2"],immaginiP["kikiS3"],
            immaginiP["kikiS4"],immaginiP["kikiS5"],immaginiP["kikiS6"],immaginiP["kikiS7"]]

      self.walkright=[
            immaginiP["kikiD0"],immaginiP["kikiD1"],immaginiP["kikiD2"],immaginiP["kikiD3"],
            immaginiP["kikiD4"],immaginiP["kikiD5"],immaginiP["kikiD6"],immaginiP["kikiD7"]]

      self.walkup=[
            immaginiP["kikiR0"],immaginiP["kikiR1"],immaginiP["kikiR2"],immaginiP["kikiR3"],
            immaginiP["kikiR4"],immaginiP["kikiR5"],immaginiP["kikiR6"],immaginiP["kikiR7"]]

      self.walkdown=[
            immaginiP["kikiF0"],immaginiP["kikiF1"],immaginiP["kikiF2"],immaginiP["kikiF3"],
            immaginiP["kikiF4"],immaginiP["kikiF5"],immaginiP["kikiF6"],immaginiP["kikiF7"]]

      self.x = x*OFFSET_FINESTRA
      self.y = y*OFFSET_FINESTRA
      self.speed = speed*OFFSET_FINESTRA
      self.fps=FPS
      #walkcount serve per le animazioni personaggio
      self.walkcount=walkcount
      self.off=OFFSET_FINESTRA

      #oggetti ottenuti
      self.oggAcido=True
      self.sbloccaP=True
      self.newroom=True
      self.oggmartello=True
      self.oggmoneta=True
      self.oggmerendina=True
      self.port1=True
      self.port2=True
      self.server=True
      self.scaff2=True
      self.scaff3=True
      self.scaff1=True
      self.flag=False
      self.lvl=False
      self.boss=False
      

#--------------------------------------------------------------------------------#


   def aggplayer(self,finestra,left,right,up,down,y,x,tipostanza,key,attivaInv,inventarioImg,oggetti):
      self.x=x
      self.y=y

      #hitbox player
      #self.rect=pygame.Rect(self.x, self.y, self.img.get_width(), self.img.get_height())
      self.rect=pygame.Rect(self.x+self.img.get_width()/3.3, self.y+self.img.get_height()/1.8, self.img.get_width()/2.4, self.img.get_height()/3.4)
      
      #stanza attuale
      self.tipost=tipostanza

      #posizione player
      txt="x: "+str(x)+" y: "+str(y)
      #print(txt)

      
#--------------------------------------------------------------------------------#


      #PLAYER MOVEMENT CON ANIMAZIONI
      if self.walkcount +1 >=self.fps:
         self.walkcount=0
            
      if left:
         finestra.blit(self.walkleft[self.walkcount//8],(self.x,self.y))
         self.walkcount+=int(self.fps/22*self.off)
         self.img= self.walkleft[0]
         #pygame.draw.rect(finestra,"red",self.rect,1)

      elif right:
         finestra.blit(self.walkright[self.walkcount//8],(self.x,self.y))
         self.walkcount+=int(self.fps/22*self.off)
         self.img= self.walkright[0]
         #pygame.draw.rect(finestra,"red",self.rect,1)

      elif up:
         finestra.blit(self.walkup[self.walkcount//8],(self.x,self.y))
         self.walkcount+=int(self.fps/22*self.off)
         self.img= self.walkup[0]
         #pygame.draw.rect(finestra,"red",self.rect,1)

      elif down:
         finestra.blit(self.walkdown[self.walkcount//8],(self.x,self.y))
         self.walkcount+=int(self.fps/22*self.off)
         self.img= self.walkdown[0]
         #pygame.draw.rect(finestra,"red",self.rect,1)

      else:
         finestra.blit(self.img,(self.x,self.y)) 
         #pygame.draw.rect(finestra,"red",self.rect,1)


#--------------------------------------------------------------------------------#


      #STANZA CHIMICA1        
      if self.tipost=="chimica1":

         #IMPORTO TUTTE LE COLLISIONI GENERALI
         collisione=collisioni(self.tipost,self.off,finestra)

         #porta chimica2
         porta1=pygame.Rect( (174.5*self.off,90.5*self.off,(246-174.5)*self.off,30*self.off) )
        # pygame.draw.rect(finestra,"red", porta1,1)

         #porta corridoio
         porta2=pygame.Rect( (34.5*self.off,516.5*self.off,30*self.off,(584.5-516.5)*self.off) )
        # pygame.draw.rect(finestra,"red", porta2,1)

         for col in collisione:
            if self.rect.colliderect(col):
               if left:
                  self.x+=self.speed
               if right:
                  self.x-=self.speed
               if up:
                  self.y+=self.speed
               if down:
                  self.y-=self.speed

         if self.rect.colliderect(porta1):
            self.tipost="chimica2"
            self.x=507.5*self.off
            self.y=550.5*self.off

         if self.rect.colliderect(porta2) and self.sbloccaP==False and self.oggAcido==False:
            dialogo("porta bloccata",finestra,self.off)
         elif self.rect.colliderect(porta2) and self.sbloccaP==False and self.oggAcido==True:
            dialogo("sciogli la maniglia",finestra,self.off)

         if self.rect.colliderect(porta2) and self.oggAcido==True and key:
            self.sbloccaP=True
         elif self.sbloccaP and self.rect.colliderect(porta2) and self.newroom==False and left:
               self.tipost="corridoio"
               self.x=1138.5*self.off
               self.y=468.5*self.off
         elif self.sbloccaP and self.rect.colliderect(porta2) and self.newroom==True and left:
               self.tipost="corridoio2"
               self.x=1138.5*self.off
               self.y=468.5*self.off


#--------------------------------------------------------------------------------#


      #stanza chimica 2
      elif self.tipost=="chimica2" :

         #importo collisioni generali
         collisione=collisioni(self.tipost,self.off,finestra)

         #porta per chimica1 
         porta1=pygame.Rect( (508*self.off,644*self.off,(570-504)*self.off,30*self.off) )
        # pygame.draw.rect(finestra,"red", porta1,1)

         #scaffale acido
         acido=pygame.Rect( (738.5*self.off,142.5*self.off,(775-734.5)*self.off,30*self.off) )
        # pygame.draw.rect(finestra,"red", acido,1)

         for col in collisione:
            if self.rect.colliderect(col):
               if left:
                  self.x+=self.speed
               if right:
                  self.x-=self.speed
               if up:
                  self.y+=self.speed
               if down:
                  self.y-=self.speed

            if self.rect.colliderect(acido) and self.oggAcido==False:
               dialogo("prendi oggetto...",finestra,self.off)
               if key:
                  self.oggAcido=True

            if self.rect.colliderect(porta1):
                  self.tipost="chimica1"
                  self.x=174.5*self.off
                  self.y=116.5*self.off


#--------------------------------------------------------------------------------#



      #STANZA corridoio            
      elif self.tipost=="corridoio" or self.tipost=="corridoio2" :

         #importo collisioni generali
         collisione=collisioni(self.tipost,self.off,finestra)
         
         #porta chimica1
         porta1=pygame.Rect( (1214.5*self.off,468.5*self.off,30*self.off,(540.5-468.5)*self.off) )
        # pygame.draw.rect(finestra,"red", porta1,1)

         #porta biblioteca
         porta2=(pygame.Rect((32.5*self.off,467.5*self.off,30*self.off,(545.5-467.5)*self.off) ))
        # pygame.draw.rect(finestra,"red", porta2,1)


         #porta finta bidelleria
         portaF=pygame.Rect( (934.5*self.off,136.5*self.off,(1014.5-934.5)*self.off,30*self.off) )
        # pygame.draw.rect(finestra,"red", portaF,1)

         #finestra da rompere
         finestraRompi=pygame.Rect( (558.5*self.off,335.5*self.off,(622.5-558.5)*self.off,30*self.off) )
        # pygame.draw.rect(finestra,"red", finestraRompi,1)

         #personaggio misterioso
         misterioso=pygame.Rect( (1135.5*self.off,165.5*self.off,(1190.5-1135.5)*self.off,(197.5-165.5)*self.off) )
        # pygame.draw.rect(finestra,"red", misterioso,1)

         #macchineetta
         macchinetta=pygame.Rect( (194.5*self.off,334.5*self.off,(282.5-194.5)*self.off,30*self.off) )
        # pygame.draw.rect(finestra,"red", macchinetta,1)

         #ascensore
         ascensore=pygame.Rect( (893.5*self.off,638.5*self.off,(962.5-893.5)*self.off,30*self.off) )
        # pygame.draw.rect(finestra,"red", ascensore,1)

         for col in collisione:
            if self.rect.colliderect(col):
               if left:
                  self.x+=self.speed
               if right:
                  self.x-=self.speed
               if up:
                  self.y+=self.speed
               if down:
                  self.y-=self.speed
                  
         #cambio stanza torna chimica1
         if self.rect.colliderect(porta1):
               self.tipost="chimica1"
               self.x=70.5*self.off
               self.y=516.5*self.off

         #collisione porta finta bidelleria in alto
         if self.rect.colliderect(portaF):
            dialogo("Impossibile da aprire...",finestra,self.off)

         #collisione personaggio misterioso
         if self.rect.colliderect(misterioso) and self.oggmoneta==False:
            dialogo("ho fame, tieni questa moneta...",finestra,self.off)
            if key:
               self.oggmoneta=True
         if self.rect.colliderect(misterioso) and self.oggmerendina==True and self.oggmartello==False:
            dialogo("tieni questo martello...",finestra,self.off)
            if key:
               self.oggmartello=True

         #collisione macchinetta
         if self.rect.colliderect(macchinetta) and self.oggmoneta==False:
            dialogo("non hai monete per acquistare...",finestra,self.off)
         elif self.rect.colliderect(macchinetta) and self.oggmoneta==True and self.oggmerendina==False:
            dialogo("compra qualcosa...",finestra,self.off)
            if key:
               self.oggmerendina=True

         #collisione finestra e cambio stanza in bidelleria interno
         if self.rect.colliderect(finestraRompi) and self.oggmartello==False:
            dialogo("finestra fragile...",finestra,self.off)
         elif self.rect.colliderect(finestraRompi) and self.oggmartello==True and self.newroom==False:
            dialogo("rompi la finestra...",finestra,self.off)
            if key:
               self.tipost="corridoio2"
               self.newroom=True
         elif self.rect.colliderect(finestraRompi) and up and self.newroom==True:
            self.tipost="bidelleria"
            self.x=503.5*self.off
            self.y=565.5*self.off

         if self.rect.colliderect(porta2) and left:
            self.tipost="biblioteca"
            self.x=1133.5*self.off
            self.y=315.5*self.off

         if self.rect.colliderect(ascensore) and self.port1==False and self.port2==False:
            dialogo("Ascensore bloccato",finestra,self.off)
         elif self.rect.colliderect(ascensore) and self.port1==False and self.port2==True:
            dialogo("Manca qualcosa...",finestra,self.off)
         elif self.rect.colliderect(ascensore) and self.port1==True and self.port2==False:
            dialogo("Manca qualcosa...",finestra,self.off)
         elif self.rect.colliderect(ascensore) and self.port1 and self.port2:
            dialogo("Non potrai tornare indietro...",finestra,self.off)
            if key:
               self.tipost="ascensore"
               self.x=600*self.off
               self.y=181*self.off

#--------------------------------------------------------------------------------#


      #STANZA BIDELLERIA             
      elif self.tipost=="bidelleria":

         #importo collisioni generali
         collisione=collisioni(self.tipost,self.off,finestra)

         #finestra torna bidelleria esterno
         finestraRotta=pygame.Rect( (503.5*self.off,645.5*self.off,(576.5-503.5)*self.off,30*self.off) )
        # pygame.draw.rect(finestra,"red", finestraRotta,1)

         #pc quest
         pc=pygame.Rect( (1060.5*self.off,302.5*self.off,(1168.5-1060.5)*self.off,(416.5-302.5)*self.off) )
        # pygame.draw.rect(finestra,"red", pc,1)

         #server
         server=pygame.Rect( (184*self.off,144*self.off,(213-184)*self.off,30*self.off) )
        # pygame.draw.rect(finestra,"red", server,1)

         for col in collisione:
            if self.rect.colliderect(col):
               if left:
                  self.x+=self.speed
               if right:
                  self.x-=self.speed
               if up:
                  self.y+=self.speed
               if down:
                  self.y-=self.speed 

         if self.rect.colliderect(finestraRotta) and down :
            self.tipost="corridoio2"
            self.x=558.5*self.off
            self.y=358.5*self.off
         
         if self.rect.colliderect(server) and self.server==False:
            dialogo("Accendi il server...",finestra,self.off)
            if key:
               self.server=True

         if self.rect.colliderect(pc) and self.server and self.port1==False:
            dialogo("Sblocca...",finestra,self.off)
            if key:
               self.port1=True
         if self.rect.colliderect(pc) and self.server==False:
            dialogo("Server offline...",finestra,self.off)
      

#--------------------------------------------------------------------------------#


      #stanza biblioteca
      elif self.tipost=="biblioteca":

         #importo collisioni generali
         collisione=collisioni(self.tipost,self.off,finestra)

         # collisione porta per corridoio
         porta1=pygame.Rect( (1215.5*self.off,320.5*self.off,30*self.off,(390.5-320.5)*self.off) )
        # pygame.draw.rect(finestra,"red", porta1,1)

         # collisione scaffale1
         scaffale1=pygame.Rect( (573.5*self.off,289.5*self.off,(617.5-573.5)*self.off,30*self.off) )
        # pygame.draw.rect(finestra,"red", scaffale1,1)

         # collisione scaffale2
         scaffale2=pygame.Rect( (673.5*self.off,482.5*self.off,(617.5-573.5)*self.off,30*self.off) )
        # pygame.draw.rect(finestra,"red", scaffale2,1)

         # collisione scaffale3
         scaffale3=pygame.Rect( (949.5*self.off,289.5*self.off,(617.5-573.5)*self.off,30*self.off) )
        # pygame.draw.rect(finestra,"red", scaffale3,1)

         for col in collisione:
            if self.rect.colliderect(col):
               if left:
                  self.x+=self.speed
               if right:
                  self.x-=self.speed
               if up:
                  self.y+=self.speed
               if down:
                  self.y-=self.speed

         if self.rect.colliderect(porta1) and right and self.newroom :
            self.tipost="corridoio2"
            self.x=73.5*self.off
            self.y=468.5*self.off

         elif self.rect.colliderect(porta1) and right and self.newroom==False :
            self.tipost="corridoio"
            self.x=73.5*self.off
            self.y=468.5*self.off


         if self.rect.colliderect(scaffale1) and self.scaff1==False:
            if self.flag==False:
               dialogo("1..",finestra,self.off)
               if self.scaff2==False and self.scaff3==False:
                  if key:
                     self.scaff1=True
               else:
                  if key:
                     self.flag=True
                     self.scaff1=False
                     self.scaff2=False
                     self.scaff3=False
            else:
               dialogo("Ordine errato ritenta",finestra,self.off)
               if key:
                  self.flag=False


         if self.rect.colliderect(scaffale2) and self.scaff2==False:
            if self.flag==False:
               dialogo("2..",finestra,self.off)
               if self.scaff3==False and self.scaff1==True:
                  if key:
                     self.scaff2=True
               else:
                  if key:
                     self.scaff1=False
                     self.scaff2=False
                     self.scaff3=False
                     self.flag=True
            else:
               dialogo("Ordine errato ritenta",finestra,self.off)
               if key:
                  self.flag=False


         if self.rect.colliderect(scaffale3) and self.scaff3==False:
            if self.flag==False:
               dialogo("3..",finestra,self.off)
               if self.scaff2==True and self.scaff1==True:
                  if key:
                     self.scaff3=True
               else:
                  if key:
                     self.scaff1=False
                     self.scaff2=False
                     self.scaff3=False
                     self.flag=True
            else:
               dialogo("Ordine errato ritenta",finestra,self.off)
               if key:
                  self.flag=False
         elif self.rect.colliderect(scaffale3) and self.scaff3:
            dialogo("Si è sbloccato qualcosa",finestra,self.off)

            if self.scaff1 and self.scaff2 and self.scaff3:
               self.port2=True
            


#--------------------------------------------------------------------------------#

      elif self.tipost=="ascensore" or self.tipost=="ascensore2":
         
         #importo collisioni generali
         collisione=collisioni(self.tipost,self.off,finestra)

         # collisione scaffale3
         porta=pygame.Rect( (612*self.off,143*self.off,(672-612)*self.off,30*self.off) )
        # pygame.draw.rect(finestra,"red", porta,1)

         for col in collisione:
            if self.rect.colliderect(col):
               if left:
                  self.x+=self.speed
               if right:
                  self.x-=self.speed
               if up:
                  self.y+=self.speed
               if down:
                  self.y-=self.speed
         
         if self.rect.colliderect(porta) and self.lvl==False:
            dialogo("Vuoi andare al 2 piano",finestra,self.off)
            if key:
               self.tipost="ascensore2"
               self.lvl=True
         elif self.rect.colliderect(porta) and self.lvl:
            dialogo("BossFight!",finestra,self.off)
            if key:
               self.boss=True
         
         if self.boss and self.rect.colliderect(porta) and up:
            self.tipost="bidelleria"


#--------------------------------------------------------------------------------#


   #Mostra inventario
      if attivaInv:
         inventarioImg.agginventario(finestra)
         if self.oggAcido:
            finestra.blit(oggetti["acido"],(500*self.off,240*self.off))
         if self.oggmoneta:
            finestra.blit(oggetti["moneta"],(610*self.off,240*self.off))
         if self.oggmerendina:
            finestra.blit(oggetti["merendina"],(720*self.off,240*self.off))
         if self.oggmartello:
            finestra.blit(oggetti["martello"],(500*self.off,350*self.off))

            #500 240 - 610 240 - 720 240
            #500 350 - 610 350 - 720 350
            #500 460 - 610 460 - 720 460




      pygame.display.update()
      return self.x,self.y,self.tipost