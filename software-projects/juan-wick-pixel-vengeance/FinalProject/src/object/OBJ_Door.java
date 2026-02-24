package object;

import entity.Entity;
import main.GamePanel;

public class OBJ_Door extends Entity{
	
	GamePanel gp;
	
	// constructor
	public OBJ_Door(GamePanel gp) {
		
		super(gp);
		this.gp = gp;
		name = "Door";
		down0 = setup("/objects/door", gp.tileSize, gp.tileSize);
		collision = true;
		
	}// end OBJ_Door()
	
	public void use(Entity entity) {
			gp.playSE(5);
			gp.player.hasKey--;
	} // end use
}// end class
