package object;

import entity.Projectile;
import main.GamePanel;

public class OBJ_NinjaStar extends Projectile{

	GamePanel gp;
	
	public OBJ_NinjaStar(GamePanel gp) {
		super(gp);
		this.gp = gp;
		
		
		name = "NinjaStar";
		speed = 15;
		maxLife = 80;
		life = maxLife;
		attack = 2;
		//useCost = 1;
		alive = false;
		getImage();
		
		solidArea.x = 22;
		solidArea.y = 22;
		solidAreaDefaultX = solidArea.x;
		solidAreaDefaultY = solidArea.y;
		solidArea.width = 28;
		solidArea.height = 28;

	}
	
	public void getImage() {
		up0 = setup("/projectile/ninjaStar_0", gp.tileSize, gp.tileSize);
		up1 = setup("/projectile/ninjaStar_1", gp.tileSize, gp.tileSize);
		down0 = setup("/projectile/ninjaStar_0", gp.tileSize, gp.tileSize);
		down1 = setup("/projectile/ninjaStar_1", gp.tileSize, gp.tileSize);
		right0 = setup("/projectile/ninjaStar_0", gp.tileSize, gp.tileSize);
		right1 = setup("/projectile/ninjaStar_1", gp.tileSize, gp.tileSize);
		left0 = setup("/projectile/ninjaStar_0", gp.tileSize, gp.tileSize);
		left1 = setup("/projectile/ninjaStar_1", gp.tileSize, gp.tileSize);
	} // end getImage
} // end class
