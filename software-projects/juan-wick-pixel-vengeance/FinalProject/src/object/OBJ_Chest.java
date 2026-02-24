package object;

import entity.Entity;
import main.GamePanel;

public class OBJ_Chest extends Entity{
	
	GamePanel gp;
	
	// constructor
	public OBJ_Chest(GamePanel gp) {
		
		super(gp);
		this.gp = gp;
		name = "Chest";
		down0 = setup("/objects/chest", gp.tileSize, gp.tileSize);
		collision = true;
		
	}// end OBJ_Chest()
	
	public void use(Entity entity) {
		gp.stopMusic();
		gp.playSE(13);
	} // end use
	
	
}// end class
