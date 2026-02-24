package object;
import entity.Entity;
import main.GamePanel;

public class OBJ_Shoes extends Entity {
	GamePanel gp;
	
	public OBJ_Shoes(GamePanel gp) {
		super(gp);
		this.gp = gp;

		name = "Shoes";
		down0 = setup("/objects/shoes", gp.tileSize, gp.tileSize);
	}// end OBJ_Shoes()

	public void use (Entity entity) {
		gp.playSE(4);
		gp.ui.addMessage("Speed increased!");
		gp.player.speed++;
	} //  end use
}
