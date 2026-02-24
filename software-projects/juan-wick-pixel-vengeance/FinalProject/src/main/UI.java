package main;

import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Font;
import java.awt.FontFormatException;
import java.awt.Graphics2D;
import java.awt.RenderingHints;
import java.awt.image.BufferedImage;
import java.io.IOException;
import java.io.InputStream;
import java.util.ArrayList;

import entity.Entity;
import object.OBJ_Heart;
import object.OBJ_Key;

public class UI {

		GamePanel gp;
		Graphics2D g2;
		Font compacta, maruMonica, minecraft;
		BufferedImage full_heart, half_heart, empty_heart;
		public boolean messageOn = false;
		public String message1 = "";
		int messageCounter1 = 0;
		ArrayList <String> message = new ArrayList<>();
		ArrayList<Integer> messageCounter = new ArrayList<>();
		public boolean gameFinished = false;
		public int commandNum = 0;
		public int titleScreenState = 0;	// 0: first screen, 1: second screen
		int subState = 0;
		
		//For displaying key 
		BufferedImage keyImage;
		
		public UI(GamePanel gp) {
			this.gp = gp;
			
			try {
				InputStream is = getClass().getResourceAsStream("/fonts/maruMonica.ttf");
				maruMonica = Font.createFont(Font.TRUETYPE_FONT, is);
				
				is = getClass().getResourceAsStream("/fonts/minecraft.ttf");
				minecraft = Font.createFont(Font.TRUETYPE_FONT, is);
				
				is = getClass().getResourceAsStream("/fonts/compacta.ttf");
				compacta = Font.createFont(Font.TRUETYPE_FONT, is);
				
			} catch (FontFormatException e) {
				e.printStackTrace();
			} catch (IOException e) {
				e.printStackTrace();
			}
			
			
			OBJ_Key key = new OBJ_Key(gp);
			keyImage = key.down0;
			
			//Create Hud Object
			Entity heart = new OBJ_Heart(gp);
			full_heart = heart.image;
			half_heart = heart.image2;
			empty_heart = heart.image3;
			
		}
		
		public void addMessage(String text) {
			message.add(text);
			messageCounter.add(0);
		} //  end showMessage
		
		public void draw(Graphics2D g2) {
			
			this.g2 = g2;
			
			g2.setFont(maruMonica);
			g2.setRenderingHint(RenderingHints.KEY_TEXT_ANTIALIASING, RenderingHints.VALUE_TEXT_ANTIALIAS_ON);
			g2.setColor(Color.black);
			g2.setFont(g2.getFont().deriveFont(Font.PLAIN, 60F));
			
			
			// MESSAGE
			if(messageOn == true) {
				g2.setFont(g2.getFont().deriveFont(30F));
				g2.setColor(Color.black);
				g2.drawString(message1, gp.tileSize/2, gp.tileSize*5);
				
				messageCounter1++;
				
				if(messageCounter1 > 120) { // text disappears after 2 sec 
					messageCounter1 = 0;
					messageOn = false;
				}
			}
			
			//TITLE STATE
			if(gp.gameState == gp.titleState) {
				drawTitleScreen();
			}
			//PLAY STATE
			if(gp.gameState == gp.playState) {
				drawPlayerLife();
				drawMessage();
			}
			//PAUSE STATE
			if(gp.gameState == gp.pauseState) {
				drawPlayerLife();
				drawPauseScreen();
			}
			// OPTIONS STATE
			if(gp.gameState == gp.optionsState) {
				drawOptionsScreen();
			}
			// GAME OVER STATE
			if(gp.gameState == gp.gameOverState) {
				drawGameOverScreen();
			}
			if(gp.gameState == gp.endGameState) {
				drawEndGameScreen();
			}

		} // end draw
		
		//Method to draw player life
		public void drawPlayerLife() {
			
			g2.drawImage(keyImage, 45, 68, gp.tileSize -5, gp.tileSize - 5, null);
			g2.drawString("x" + gp.player.hasKey, 95, 115);
			
			//gp.player.life = 6;
			
			int x = gp.tileSize/4;
			int y = gp.tileSize/8;
			int i = 0;
			
			//Draw Blank Heart
			while(i < gp.player.maxLife/2) {
				g2.drawImage(empty_heart, x, y, null);
				i++;
				x += gp.tileSize;
			}
			//Reset
			x = gp.tileSize/4;
			y = gp.tileSize/8;
			i = 0;
			
			//Draw Current Life
			while(i < gp.player.life) {
				g2.drawImage(half_heart, x,  y,  null);
				i++;
				if(i < gp.player.life) {
					g2.drawImage(full_heart, x, y, null);
				}
				i++;
				x += gp.tileSize;
			}
			
		}
		
		
		public void drawMessage() {
			
			int messageX = gp.tileSize;
			int messageY = gp.tileSize*4;
			g2.setFont(g2.getFont().deriveFont(Font.BOLD, 32F));
			
			for (int i = 0; i < message.size(); i++) {
				
				if(message.get(i) != null) {
					g2.setColor(Color.white);
					g2.drawString(message.get(i), messageX+2, messageY+2);
					g2.setColor(Color.black);
					g2.drawString(message.get(i), messageX, messageY);
					
					int counter = messageCounter.get(i) + 1;	// messageCounter++
					messageCounter.set(i, counter);				// set the counter to the array
					messageY += 50;
					
					if(messageCounter.get(i) > 180) {
						message.remove(i);
						messageCounter.remove(i);
					}
				}
				
			} // end for
			
			
			
		}// end drawMessage
		
		public void drawTitleScreen() {
			
			if(titleScreenState == 0) {
				g2.setFont(compacta);
				g2.setColor(new Color(153,0,0));
				g2.fillRect(0, 0, gp.screenWidth, gp.screenHeight);
				//TITLE NAME
				
				g2.setFont(g2.getFont().deriveFont(Font.ITALIC | Font.BOLD,170F));
				String text = "JUAN WICK";
				int x = getXforCenteredText(text);
				int y = (gp.tileSize*3);
				
				//SHADOW
				g2.setColor(Color.black);
				g2.drawString(text, x+5, y+5);
				
				//MAIN COLOR
				g2.setColor(Color.white);
				g2.drawString(text, x, y);
				
				//JUAN WICK IMAGE
				x = gp.screenWidth/2 - (gp.tileSize*2)/2;
				y += gp.tileSize;
				g2.drawImage(gp.player.TitleScreen, 110, 160, 1000, 270, null);	// x-coordinate, y-coordinate, width, height
				
				
				
				//MENU
				g2.setFont(maruMonica);
				g2.setFont(g2.getFont().deriveFont(Font.BOLD,60F));
				
				text = "NEW GAME";
				x = getXforCenteredText(text);
				y += gp.tileSize * 6;
				g2.drawString(text, x, y);
				if(commandNum == 0 ) {
					g2.drawString(">", x-gp.tileSize, y);  //draw image to use image
				}
				
				text = "LOAD GAME";
				x = getXforCenteredText(text);
				y += gp.tileSize;
				g2.drawString(text, x, y);
				if(commandNum == 1 ) {
					g2.drawString(">", x-gp.tileSize, y);  //draw image to use image
				}
				
				text = "QUIT";
				x = getXforCenteredText(text);
				y += gp.tileSize;
				g2.drawString(text, x, y);
				if(commandNum == 2 ) {
					g2.drawString(">", x-gp.tileSize, y);  //draw image to use image
				} // end if
			} // end bigger if
			
			else if (titleScreenState == 1) {
				
				// SKIN SELECTION SCREEN
				g2.setColor(Color.white);
				g2.setFont(g2.getFont().deriveFont(60F));
				
				String text = "Select the suit for           !";
				int x = getXforCenteredText(text);
				int y = gp.tileSize * 4;
				g2.drawString(text, x, y);
				
				
				text = "Gray Suit";
				x = getXforCenteredText(text);
				y += gp.tileSize*2; 
				g2.drawString(text, x, y);
				if(commandNum == 0) {
					g2.drawString(">", x-gp.tileSize, y);
				}
				
				text = "Blue Suit";
				x = getXforCenteredText(text);
				y += gp.tileSize+5; 
				g2.drawString(text, x, y);
				if(commandNum == 1) {
					g2.drawString(">", x-gp.tileSize, y);
				}
				
				text = "Black Suit";
				x = getXforCenteredText(text);
				y += gp.tileSize+5; 
				g2.drawString(text, x, y);
				if(commandNum == 2) {
					g2.drawString(">", x-gp.tileSize, y);
				}
				
				text = "Back";
				x = getXforCenteredText(text);
				y += gp.tileSize * 2; 
				g2.drawString(text, x, y);
				if(commandNum == 3) {
					g2.drawString(">", x-gp.tileSize, y);
				}
				
				g2.setFont(compacta);
				g2.setFont(g2.getFont().deriveFont(Font.ITALIC,45F));
				g2.setColor(Color.yellow);
				g2.drawString("JUAN WICK", 742 ,gp.tileSize*4);
				
				
			} // end else if
			
			
		} // end drawTitleScreen
		
		public void drawPauseScreen() {
			g2.setFont(minecraft);
			g2.setFont(g2.getFont().deriveFont(Font.PLAIN, 80F));
			String text = "PAUSED";
			int x = getXforCenteredText(text);
			int y = gp.screenHeight/2;
			g2.drawString(text, x, y);
		} //  end drawPauseScreen
		
		public void drawGameOverScreen() {
			
			g2.setFont(compacta);
			g2.setColor(new Color(0,0,0,150));
			g2.fillRect(0,0, gp.screenWidth, gp.screenHeight);
			
			int x;
			int y;
			String text;
			g2.setFont(g2.getFont().deriveFont(Font.BOLD | Font.ITALIC, 160f));
			
			text = "Game Over";
			
			// Shadow
			g2.setColor(Color.black);
			x = getXforCenteredText(text);
			y = gp.tileSize*4;
			g2.drawString(text, x, y);
			
			// Game Over string
			g2.setColor(Color.white);
			g2.drawString(text, x-4, y-4);

			// retry
			g2.setFont(maruMonica);
			g2.setFont(g2.getFont().deriveFont(Font.BOLD, 60f));
			text = "Retry";
			x = getXforCenteredText(text);
			y += gp.tileSize*4;
			g2.drawString(text, x, y);
			if(commandNum == 0) {
				g2.drawString(">", x-40, y);
			}
			
			
			// Back to Title Screen
			text = "Quit";
			x = getXforCenteredText(text);
			y += 55;
			g2.drawString(text, x, y);
			if(commandNum == 1) {
				g2.drawString(">", x-40, y);
			}
			
		} // end drawGameOverScreen
		
		public void drawOptionsScreen() {
			g2.setFont(minecraft);
			g2.setColor(Color.white);
			g2.setFont(g2.getFont().deriveFont(Font.PLAIN, 40F));
			
			// SUB WINDOW
			int frameX = gp.tileSize*7;
			int frameY = gp.tileSize;
			int frameWidth = gp.tileSize*8;
			int frameHeight = gp.tileSize*12;
			drawSubWindow(frameX, frameY, frameWidth, frameHeight);
			
			switch(subState) {
			case 0:	options_top( frameX,  frameY);	break;
			case 1: options_control( frameX,  frameY);	break;
			case 2: options_endGameConfirmation(frameX,  frameY);	break;
			} // end switch
			
			gp.keyH.enterPressed = false;
			
		} // end drawOptionsScreen
		
		public void drawEndGameScreen() {

			g2.setFont(compacta);
			g2.setColor(new Color(0,0,0,150));
			g2.fillRect(0,0, gp.screenWidth, gp.screenHeight);
			
			int x;
			int y;
			String text;
			g2.setFont(g2.getFont().deriveFont(Font.BOLD | Font.ITALIC, 160f));
			
			text = "WELL DONE MR. WICK";
			
			// Shadow
			g2.setColor(Color.blue);
			x = getXforCenteredText(text);
			y = gp.tileSize*4;
			g2.drawString(text, x, y);
			
			// Game Over string
			g2.setColor(Color.white);
			g2.drawString(text, x-4, y-4);

			// EXIT
			g2.setFont(maruMonica);
			g2.setFont(g2.getFont().deriveFont(Font.BOLD, 60f));
			text = "Back to Title Screen";
			x = getXforCenteredText(text);
			y += gp.tileSize*4;
			g2.drawString(text, x, y);
			if(commandNum == 0) {
				g2.drawString(">", x-40, y);
			}
			
			// Back to Title Screen
			text = "Exit game";
			x = getXforCenteredText(text);
			y += 70;
			g2.drawString(text, x, y);
			if(commandNum == 1) {
				g2.drawString(">", x-40, y);
			}
			
		} // end drawGameOverScreen
		
		public void options_top(int frameX, int frameY) {
			
			int textX;
			int textY;
			
			// TITLE
			String text = "Options";
			textX = getXforCenteredText(text);
			textY = frameY + gp.tileSize+10;
			g2.drawString(text, textX, textY);
			
			g2.setFont(maruMonica);
			g2.setColor(Color.white);
			g2.setFont(g2.getFont().deriveFont(Font.BOLD, 43F));

			
			// MUSIC
			textX = frameX + gp.tileSize;
			textY += gp.tileSize*2+10;
			g2.drawString("Music", textX, textY);
			if (commandNum == 0) {
				g2.drawString(">", textX-25, textY);
			}
			
			// SE
			textX = frameX + gp.tileSize;
			textY += gp.tileSize + 20;
			g2.drawString("SE", textX, textY);
			if (commandNum == 1) {
				g2.drawString(">", textX-25, textY);
			}
			
			// CONTROLS
			textX = frameX + gp.tileSize;
			textY += gp.tileSize + 20;
			g2.drawString("Controls", textX, textY);
			if (commandNum == 2) {
				g2.drawString(">", textX-25, textY);
				if(gp.keyH.enterPressed == true) {
					subState = 1;
					commandNum = 0;
				}
			}
			
			// END GAME
			textX = frameX + gp.tileSize;
			textY += gp.tileSize + 20;
			g2.drawString("End Game", textX, textY);
			if (commandNum == 3) {
				g2.drawString(">", textX-25, textY);
				if(gp.keyH.enterPressed == true) {
					subState = 2;
					commandNum = 0;
				}
			}
			
			// BACK
			textX = frameX + gp.tileSize;
			textY += gp.tileSize*3;
			g2.drawString("Back", textX, textY);
			if (commandNum == 4) {
				g2.drawString(">", textX-25, textY);
				if(gp.keyH.enterPressed == true) {
					gp.gameState = gp.playState;
					commandNum = 0;
				}
			}
			
			// MUSIC VOLUME
			textX = frameX + gp.tileSize*4;
			textY = frameY + gp.tileSize*3 - 10;
			g2.drawRect(textX, textY, 180, 30);		//	180/5 = 36
			int volumeWidth = 36* gp.music.volumeScale;
			g2.fillRect(textX, textY, volumeWidth, 30);
			
			
			
			// SE VOLUME
			textY += gp.tileSize+17;
			g2.drawRect(textX, textY, 180, 30);
			volumeWidth = 36* gp.se.volumeScale;
			g2.fillRect(textX, textY, volumeWidth, 30);
			
			gp.config.saveConfig();
			
		} // end options_top
		
		public void options_control(int frameX, int frameY) {
			
			
			int textX;
			int textY;
			
			// TITLE
			String text = "Controls";
			textX = getXforCenteredText(text);
			textY = frameY + gp.tileSize+10;
			g2.drawString(text, textX, textY);
			
			g2.setFont(maruMonica);
			g2.setColor(Color.white);
			g2.setFont(g2.getFont().deriveFont(Font.BOLD, 36F));
			
			textX = frameX + gp.tileSize;
			textY += gp.tileSize*2;
			g2.drawString("Move", textX, textY); textY += gp.tileSize+40;
			g2.drawString("Confirm/Shot", textX, textY); textY += gp.tileSize+40;
			g2.drawString("Pause", textX, textY); textY += gp.tileSize+40;
			g2.drawString("Options", textX, textY); textY += gp.tileSize+40;			
			
			
			textX = frameX + gp.tileSize*6;
			textY = frameY + gp.tileSize*3+9;
			g2.drawString("WASD", textX, textY); textY += gp.tileSize+40;			
			g2.drawString("ENTER", textX, textY); textY += gp.tileSize+40;			
			g2.drawString("P", textX, textY); textY += gp.tileSize+40;			
			g2.drawString("ESC", textX, textY); textY += gp.tileSize+40;			
			
			
			// BACK
			textX = frameX + gp.tileSize;
			textY = frameY + gp.tileSize*11;
			g2.drawString("Back", textX, textY);
			if (commandNum == 0) {
				g2.drawString(">", textX-25, textY);
				if(gp.keyH.enterPressed == true) {
					subState = 0;
					commandNum = 2; 
				}
			
			}
			
			
		} //  options_control
		
		public void options_endGameConfirmation(int frameX, int frameY) {
			
			g2.setFont(maruMonica);
			g2.setColor(Color.white);
			g2.setFont(g2.getFont().deriveFont(Font.BOLD, 36F));
			
			int textX = frameX + gp.tileSize;
			int textY = frameY + gp.tileSize*3;
			
			String currentDialogue = "Quit the game and \nreturn to the title screen?";
			
			for (String line: currentDialogue.split("\n")) {
				g2.drawString(line, textX, textY);
				textY += 40;
			}
			
			// YES
			String text = "Yes";
			textX = getXforCenteredText(text);
			textY += gp.tileSize*3;
			g2.drawString(text, textX, textY);
			if (commandNum == 0) {
				g2.drawString(">", textX-25, textY);
				if(gp.keyH.enterPressed == true) {
					subState = 0;
					gp.gameState = gp.titleState;
					gp.ui.titleScreenState = 0;
					gp.stopMusic();
					gp.restart();
				}
			}
			
			
			// NO
			text = "No";
			textX = getXforCenteredText(text);
			textY += gp.tileSize;
			g2.drawString(text, textX, textY);
			if (commandNum == 1) {
				g2.drawString(">", textX-25, textY);
				if(gp.keyH.enterPressed == true) {
					subState = 0;
					commandNum = 3;
				}
			}
			
			
			
		} // end options_endGameConfirmation
		
		public void drawSubWindow(int x, int y, int width, int height) {
			
			Color c = new Color(0,0,0,220);
			g2.setColor(c);
			g2.fillRoundRect(x, y, width, height, 35, 35);
			
			c = new Color(255, 255, 255);
			g2.setColor(c);
			g2.setStroke(new BasicStroke(5));
			g2.drawRoundRect(x+5, y+5, width-10, height-10, 25, 25);
			
		} // end drawSubWindow

		public int getXforCenteredText(String text) {
			
			int length = (int)g2.getFontMetrics().getStringBounds(text, g2).getWidth();
			int x = gp.screenWidth/2 - length/2;
			return x;
			
		} // end getXforCenteredText
		
} // end class









