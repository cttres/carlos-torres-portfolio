package enemy;

import java.util.Random;

import entity.Entity;
import main.GamePanel;
import object.OBJ_BlueHeart;
import object.OBJ_Heart;
import object.OBJ_NinjaStar;
import object.OBJ_Shotgun;

/**
 * Represents a Blue Ninja enemy in the game.
 * Extends the Entity class.
 *
 * @author Horacio Gonzalez
 * @author Erick Nevarez
 * @author Erick Lopez
 * @author Carlos Torres
 * @version 1.0
 * @since December 1, 2023
 */
public class ENEM_BlueNinja extends Entity {

    GamePanel gp;

    /**
     * Constructs a Blue Ninja object.
     *
     * @param gp The GamePanel where the Blue Ninja exists.
     */
    public ENEM_BlueNinja(GamePanel gp) {
        super(gp);

        this.gp = gp;

        type = 2;
        name = "Ninja";
        speed = 9;          // or maybe 6, we'll see
        maxLife = 6;
        life = maxLife;
        attack = 4;
        defense = 0;
        projectile = new OBJ_NinjaStar(gp);

        solidArea.x = 11;
        solidArea.y = 5;
        solidArea.width = 32;
        solidArea.height = 55;
        solidAreaDefaultX = solidArea.x;
        solidAreaDefaultY = solidArea.y;

        getImage();
    } // end constructor

    /**
     * Loads images for the Blue Ninja in different directions.
     */
    public void getImage() {

        // setupPlayer = setup using the player size, to keep proportions of the ninjas

        up0 = setup("/enemy/blueninja_up_0", gp.tileSize, gp.tileSize);
        up1 = setup("/enemy/blueninja_up_1", gp.tileSize, gp.tileSize);
        down0 = setup("/enemy/blueninja_down_0", gp.tileSize, gp.tileSize);
        down1 = setup("/enemy/blueninja_down_1", gp.tileSize, gp.tileSize);
        right0 = setup("/enemy/blueninja_right_0", gp.tileSize, gp.tileSize);
        right1 = setup("/enemy/blueninja_right_1", gp.tileSize, gp.tileSize);
        left0 = setup("/enemy/blueninja_left_0", gp.tileSize, gp.tileSize);
        left1 = setup("/enemy/blueninja_left_1", gp.tileSize, gp.tileSize);

    } // end getImage

    /**
     * Defines the action of the Blue Ninja, including movement and projectile launching.
     */
    public void setAction() {

        // Very simple AI
        actionLockCounter++;

        if (actionLockCounter == 120) {

            Random random = new Random();
            int i = random.nextInt(100) + 1;    // pick a number from 1 to 100

            if (i <= 25) {
                direction = "up";
            }
            if (i > 25 && i <= 50) {
                direction = "down";
            }
            if (i > 50 && i <= 75) {
                direction = "left";
            }
            if (i > 75 && i <= 100) {
                direction = "right";
            }

            actionLockCounter = 0;

        } // end if

        int i = new Random().nextInt(100) + 1;
        if (i > 99 && projectile.alive == false && shotAvailableCounter == 50) {
            projectile.set(worldX, worldY, direction, true, this);
            gp.projectileList.add(projectile);
            shotAvailableCounter = 0;
        }

    } // end setAction

    /**
     * Defines the Blue Ninja's reaction to taking damage.
     */
    public void damageReaction() {

        actionLockCounter = 0;

        Random random = new Random();
        int i = random.nextInt(4) + 1;    // pick a number from 1 to 4

        if (i == 1) {
            direction = "down";
        } else if (i == 2) {
            direction = "up";
        } else if (i == 3) {
            direction = "right";
        } else if (i == 4) {
            direction = "left";
        }
        // else if ( i == 5) {
        //     direction = gp.player.direction;     // enemy will run away from player
        // }

    } // end damageReaction

    /**
     * Checks if the Blue Ninja should drop an item after defeat.
     */
    public void checkDrop() {

        // CAST A DIE
        int i = new Random().nextInt(100) + 1;

        // SET THE ENEMY DROP
        if (i < 50) {
            dropItem(new OBJ_Heart(gp));
        } else if (i >= 50 && i < 75) {
            dropItem(new OBJ_BlueHeart(gp));
        } else if (i >= 75 && i < 90) {
            dropItem(new OBJ_Shotgun(gp));
        }

    } // end checkDrop

} // end class
