package entity;

import main.GamePanel;

/**
 * The Projectile class represents a projectile entity in the game.
 * It extends the Entity class and encapsulates the attributes and behavior of projectiles.
 *
 * @version 1.0
 * @since December 1, 2023
 * @author Horacio Gonzalez
 * @author Erick Nevarez
 * @author Erick Lopez
 * @author Carlos Torres
 */
public class Projectile extends Entity {

    /** The entity that fired the projectile. */
    Entity user;

    /**
     * Constructs a Projectile object with the specified GamePanel.
     *
     * @param gp The GamePanel instance.
     */
    public Projectile(GamePanel gp) {
        super(gp);
        // TODO: Initialization code if needed
    }

    /**
     * Sets the initial parameters for the projectile.
     *
     * @param worldX     The initial X-coordinate in the game world.
     * @param worldY     The initial Y-coordinate in the game world.
     * @param direction  The initial direction of the projectile (up, down, left, right).
     * @param alive      The initial state of the projectile's existence.
     * @param user       The entity that fired the projectile.
     */
    public void set(int worldX, int worldY, String direction, boolean alive, Entity user) {
        this.worldX = worldX;
        this.worldY = worldY;
        this.direction = direction;
        this.alive = alive;
        this.user = user;
        this.life = this.maxLife;
    } // end set

    /**
     * Updates the projectile's position, checks for collisions, and handles interactions.
     *
     * If the projectile's user is the player, it checks for enemy collisions and damages enemies accordingly.
     * If the user is not the player, it checks for collisions with the player and damages the player if applicable.
     * The projectile's position is updated based on its direction, and its life is decremented.
     */
    public void update() {
        // Check if the user is the player and handle enemy collisions
        if (user == gp.player) {
            int enemyIndex = gp.cChecker.checkEntity(this, gp.enemy);
            if (enemyIndex != 999) {
                gp.player.damageEnemy(enemyIndex);
                alive = false;
            }
        }

        // Check if the user is not the player and handle player collisions
        if (user != gp.player) {
            boolean contactPlayer = gp.cChecker.checkPlayer(this);
            if (gp.player.invincible == false && contactPlayer == true) {
                damagePlayer(attack);
                alive = false;
            }
        }

        // Update the projectile's position based on its direction
        switch (direction) {
            case "up":
                worldY -= speed;
                break;
            case "down":
                worldY += speed;
                break;
            case "left":
                worldX -= speed;
                break;
            case "right":
                worldX += speed;
                break;
        } // end switch

        // Decrease the projectile's life and mark it as not alive if life is zero or less
        life--;
        if (life <= 0) {
            alive = false;
        }

        // Manage sprite animation
        spriteCounter++;
        if (spriteCounter > 12) {
            if (spriteNum == 1) {
                spriteNum = 2;
            } else if (spriteNum == 2) {
                spriteNum = 1;
            }
            spriteCounter = 0;
        }
    } // end update
} // end class
