/*
 * Parent class for all object classes that we will create
 */

package object;

import java.awt.Graphics2D;
import java.awt.Rectangle;
import java.awt.image.BufferedImage;

import main.GamePanel;
import main.UtilityTool;

public class SuperObject {

	
	public BufferedImage image, image2, image3;
	public String name;
	public boolean collision = false;
	public int worldX, worldY;
	public Rectangle solidArea = new Rectangle(0,0,48,48);
	public int solidAreaDefaultX = 0;
	public int solidAreaDefaultY = 0;
	UtilityTool uTool = new UtilityTool();
	
	//Method to draw the objects
	public void draw(Graphics2D g2, GamePanel gp) {
		
		int screenX = worldX - gp.player.worldX + gp.player.screenX;	// Position on screen
		int screenY = worldY - gp.player.worldY + gp.player.screenY;	// Position on screen
		
		if(worldX + gp.tileSize > gp.player.worldX - gp.player.screenX &&
		   worldX - gp.tileSize < gp.player.worldX + gp.player.screenX &&
		   worldY + gp.tileSize > gp.player.worldY - gp.player.screenY &&
		   worldY - gp.tileSize < gp.player.worldY + gp.player.screenY)	{
			
			g2.drawImage(image, screenX, screenY, gp.tileSize, gp.tileSize, null);

		} //end if
	} // end draw()
} // end class
