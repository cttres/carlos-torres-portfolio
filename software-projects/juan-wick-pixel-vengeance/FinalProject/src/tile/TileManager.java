package tile;

import java.awt.Graphics2D;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

import javax.imageio.ImageIO;
import main.GamePanel;
import main.UtilityTool;

public class TileManager {

	GamePanel gp;
	public Tile[] tile;			//Single tile or texture
	public int mapTileNum[][];		//Two-Dimentional Array for column and row
	
	public TileManager(GamePanel gp) {
		this.gp = gp;
		
//**********The number in the array "Tile" in the next line, limits the amount of tiles aka textures**********
		tile = new Tile[18];	
		mapTileNum = new int[gp.maxWorldCol][gp.maxWorldRow];
		
		getTileImage();
		loadMap("/maps/map001.txt");
	}//End TileManager
	
	//Declaration and import of the textures or tiles.
	//**********MUST BE .PNG AND STORED IN RESOURCES UNDER TILES**********
	public void getTileImage() {
		
		// (NUMBER,   NAME,   COLLISION)
//		setup(0, "RedWoodTile", false);
//		setup(1, "WallTile", true);
//		setup(2, "WhiteFloor", false);
//		setup(3, "WhiteWoodTile", false);
//		setup(4, "WindowScreen", true);
//		setup(5, "WindowTile", false);
		
		setup(0, "Blank", true);
		setup(1, "BlueFloor", false);
		setup(2, "carpet", false);
		setup(3, "CementWall", false);
		setup(4, "ChessFloor", false);
		setup(5, "concrete", false);
		setup(6, "Dirt", false);
		setup(7, "Grass", false);
		setup(8, "Gravel", false);
		setup(9, "GreenTileFloor", false);
		setup(10, "pinkTile", false);
		setup(11, "redTile", false);
		setup(12, "RockWall", false);
		setup(13, "Water", true);
		setup(14, "WhiteFloor", false);
		setup(15, "WhiteWoodTile", false);
		setup(16, "WindowScreen", false);
		setup(17, "wood1", false);


		
			
	}//End getTileImage
	
	
	public void setup(int index, String imageName, boolean collision){
		
		UtilityTool uTool = new UtilityTool();
		
		try {
			
			tile[index] = new Tile();
			tile[index].image = ImageIO.read(getClass().getResourceAsStream("/tiles/" + imageName + ".png"));
			tile[index].image = uTool.scaleImage(tile[index].image, gp.tileSize, gp.tileSize);
			tile[index].collision = collision;
			
		} catch(IOException e) {
			e.printStackTrace();
		}
		
		
	} //  end setup
	
	
	
	//Loading of Maps
	public void loadMap(String filePath) {				//filePath String automation for multiple maps
		
		try {
			InputStream is = getClass().getResourceAsStream(filePath);
			BufferedReader br = new BufferedReader(new InputStreamReader(is));
			
			int col = 0;
			int row = 0;
			
			//**********"maxScreenCol" and "maxScreenRow" are declared in GamePanel**********
			while(col < gp.maxWorldCol && row < gp.maxWorldRow) {
				String line = br.readLine();
				
				while(col < gp.maxWorldCol) {
					String numbers[] = line.split(" ");	//Space must be placed in 2D array to recognize and properly Skip.
					
					int num = Integer.parseInt(numbers[col]);
					
					mapTileNum[col][row] = num;
					col++;
				}//End While
				if(col == gp.maxWorldCol) {
					col = 0;
					row++;
				}//End if
			}//End While
			
		}catch(Exception e) {
			e.printStackTrace();
			}//End try
	}//End loadMap
	public void draw(Graphics2D g2) {		//**********SEPARATION BETWEEN TILES IS 66 PIXELS**********
		
		int worldCol = 0;
		int worldRow = 0;
		
		
		while(worldCol < gp.maxWorldCol && worldRow < gp.maxWorldRow ) {
			
			int tileNum = mapTileNum[worldCol][worldRow];
			
			int worldX = worldCol * gp.tileSize;							// Position on the map
			int worldY = worldRow * gp.tileSize;							// Position on the map
			int screenX = worldX - gp.player.worldX + gp.player.screenX;	// Position on screen
			int screenY = worldY - gp.player.worldY + gp.player.screenY;	// Position on screen
			
			// Stop moving the camera at the edge
			if(gp.player.screenX > gp.player.worldX) {
				screenX = worldX;
			}
			
			if(gp.player.screenY > gp.player.worldY) {
				screenY = worldY;
			}
			int rightOffset = gp.screenWidth - gp.player.screenX;
			if(rightOffset > gp.worldWidth - gp.player.worldX) {
				screenX = gp.screenWidth - (gp.worldWidth - worldX);
			}
			int bottomOffset = gp.screenHeight - gp.player.screenY;
			if(bottomOffset > gp.worldHeight - gp.player.worldY) {
				screenY = gp.screenHeight - (gp.worldHeight - worldY);
			}
			
			
			
			if(worldX + gp.tileSize > gp.player.worldX - gp.player.screenX &&
			   worldX - gp.tileSize < gp.player.worldX + gp.player.screenX &&
			   worldY + gp.tileSize > gp.player.worldY - gp.player.screenY &&
			   worldY - gp.tileSize < gp.player.worldY + gp.player.screenY)	{
				
				g2.drawImage(tile[tileNum].image, screenX, screenY, null);

			} //end if
			
			else if (gp.player.screenX > gp.player.worldX || 
					 gp.player.screenY > gp.player.worldY ||
					 rightOffset > gp.worldWidth - gp.player.worldX || 
					 bottomOffset > gp.worldHeight - gp.player.worldY) {
				
				g2.drawImage(tile[tileNum].image, screenX, screenY, null);

			} // end else-if
					
			worldCol++;
			
			if(worldCol == gp.maxWorldCol) {
				worldCol = 0;
				worldRow++;
			}//End if
		}//End While	
	}//End Draw
} // end class
