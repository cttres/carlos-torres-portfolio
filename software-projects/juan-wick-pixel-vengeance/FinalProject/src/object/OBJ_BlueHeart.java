package object;

import entity.Entity;
import main.GamePanel;

public class OBJ_BlueHeart extends Entity {
	GamePanel gp;

	// constructor
	public OBJ_BlueHeart(GamePanel gp) {
		super(gp);
		this.gp = gp;

		name = "BlueHeart";
		down0 = setup("/objects/blue_heart", gp.tileSize, gp.tileSize);
	}// end OBJ_Heart()

	public void use (Entity entity) {
		gp.playSE(4);
		gp.ui.addMessage("Full Life recovered!");
		gp.player.restoreLife();
	} //  end use
}


