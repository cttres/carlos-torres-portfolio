package object;


import entity.Entity;
import main.GamePanel;

public class OBJ_Heart extends Entity {
	
	GamePanel gp;
	
	// constructor
	public OBJ_Heart(GamePanel gp) {
		super(gp);
		this.gp = gp;
		
		name = "Heart";
		down0 = setup("/objects/full_heart", gp.tileSize, gp.tileSize);
		image = setup("/objects/full_heart", gp.tileSize, gp.tileSize);
		image2 = setup("/objects/half_heart", gp.tileSize, gp.tileSize);
		image3 = setup("/objects/empty_heart", gp.tileSize, gp.tileSize);
		
	}// end OBJ_Heart()
	
	public void use (Entity entity) {
		gp.playSE(4);
		gp.ui.addMessage("Life recovered!");
		gp.player.life += 2;
	} //  end use
}// end class
