package object;


import entity.Entity;
import main.GamePanel;

public class OBJ_Key extends Entity {
	
	GamePanel gp;
	
	// constructor
	public OBJ_Key(GamePanel gp) {
		super(gp);
		this.gp = gp;
		
		type = 3;
		name = "Key";
		down0 = setup("/objects/key", gp.tileSize, gp.tileSize);
				
		
	} // end OBJ_Key()
	
	public void use (Entity entity) {
		gp.playSE(6);
		gp.ui.addMessage("Got a " + name + "!");
		gp.player.hasKey++;
		gp.ui.addMessage("OPEN THE DOOR!");
		System.out.println("Key:" + gp.player.hasKey);
	} //  end use
	
	
	
	
} // end class
