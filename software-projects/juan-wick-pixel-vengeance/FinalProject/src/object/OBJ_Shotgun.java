package object;

import entity.Entity;
import main.GamePanel;

public class OBJ_Shotgun extends Entity{

	GamePanel gp;
	
	public OBJ_Shotgun(GamePanel gp) {
		super(gp);
		this.gp = gp;

		name = "Shotgun";
		down0 = setup("/objects/gun", gp.tileSize, gp.tileSize);
	}
	
	public void use (Entity entity) {
		gp.playSE(4);
		gp.ui.addMessage("Damage increased!");
		gp.player.attack += 1;
		
	} //  end use

}
