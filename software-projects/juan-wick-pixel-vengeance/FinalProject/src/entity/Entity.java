/**
 * The Entity class serves as a fundamental blueprint for various in-game characters,
 * including players, enemies, and NPCs. It encapsulates essential properties and
 * behavior shared by these entities.
 *
 * @author Horacio Gonzalez
 * @author Erick Nevarez
 * @author Erick Lopez
 * @author Carlos Torres
 * @version 1.0
 * @since December 1, 2023
 */
package entity;

import java.awt.AlphaComposite;
import java.awt.Color;
import java.awt.Graphics2D;
import java.awt.Rectangle;
import java.awt.image.BufferedImage;
import java.io.IOException;

import javax.imageio.ImageIO;

import main.GamePanel;
import main.UtilityTool;

public class Entity {

    GamePanel gp;

    // Sprite images for different directions
    public BufferedImage up0, up1, down0, down1, left0, left1, right0, right1, TitleScreen;
    // Hit-box for collision detection (you can overwrite the hit-box on the designated class;)
    public Rectangle solidArea = new Rectangle(0, 0, 48, 48);
    public int solidAreaDefaultX, solidAreaDefaultY;
    public BufferedImage image, image2, image3;
    public boolean collision = false;

    // STATE
    public int spriteNum = 1; // Total number of sprites
    public int worldX, worldY; // Current world position
    public String direction = "down"; // Current facing direction
    public boolean collisionOn = false; // Flag to enable collision detection
    public boolean invincible = false;
    boolean attacking = false;
    public boolean alive = true;
    public boolean dying = false;
    boolean hpBarOn = false;

    // COUNTER
    public int spriteCounter = 0; // Counter for sprite animation
    public int actionLockCounter = 0;
    public int invincibleCounter = 0;
    int dyingCounter = 0;
    int hpBarCounter = 0;
    public int shotAvailableCounter = 0;

    // CHARACTER ATTRIBUTES
    public int maxLife;
    public int life;
    public int type; // 0 = player, 1 = NPC (if added), 2 = enemy, 3 = itemPickup
    public String name;
    public int speed; // Movement speed
    public Projectile projectile;

    // MAYBE DELETED
    public int attack;
    public int defense;

    // ITEM ATTRIBUTES
    public int attackValue;
    public int defenseValue;

    /**
     * Constructs an Entity object.
     *
     * @param gp The GamePanel where the Entity exists.
     */
    public Entity(GamePanel gp) {
        this.gp = gp;
    } // end constructor

    // To be overwritten
    public void setAction() {
    }

    public void damageReaction() {
    }

    public void use(Entity entity) {
    }

    public void checkDrop() {
    }

    public void dropItem(Entity droppedItem) {

        for (int i = 0; i < gp.obj.length; i++) {
            if (gp.obj[i] == null) {
                gp.obj[i] = droppedItem;
                gp.obj[i].worldX = worldX; // Dead enemy's worldX
                gp.obj[i].worldY = worldY; // Dead enemy's worldY
                break;
            }
        }

    } // end dropItem

    /**
     * Updates the state of the Entity.
     */
    public void update() {
        setAction();

        collisionOn = false;
        gp.cChecker.checkTile(this);
        gp.cChecker.checkObject(this, false);
        gp.cChecker.checkEntity(this, gp.enemy);
        boolean contactPlayer = gp.cChecker.checkPlayer(this);

        // If enemy is having contact with player
        if (this.type == 2 && contactPlayer) {
            damagePlayer(attack);
        }

        // If no collision, update the player's position
        if (!collisionOn) {

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
        } // end if collisionOn

        // Manage sprite animation
        spriteCounter++;
        if (spriteCounter > 12) {
            if (spriteNum == 1) {
                spriteNum = 2;
            } else if (spriteNum == 2) {
                spriteNum = 1;
            }
            spriteCounter = 0;
        } // end if spriteCounter > 12

        if (invincible) {
            invincibleCounter++;
            if (invincibleCounter > 40) {
                invincible = false;
                invincibleCounter = 0;
            }
        } // end if
        if (shotAvailableCounter < 50) {
            shotAvailableCounter++;
        }
    } // end update

    /**
     * Damages the player based on the attack value of the Entity.
     *
     * @param attack The attack value of the Entity.
     */
    public void damagePlayer(int attack) {
        if (!gp.player.invincible) {
            // Player can receive damage
            gp.playSE(10);

            int damage = attack - gp.player.defense;
            if (damage < 0) {
                damage = 0;
            }
            gp.player.life -= damage;
            gp.player.invincible = true;
        }

    } // end damagePlayer

    /**
     * Draws the Entity on the screen.
     *
     * @param g2 The Graphics2D object to draw on.
     */
    public void draw(Graphics2D g2) {

        BufferedImage image = null;
        int screenX = worldX - gp.player.worldX + gp.player.screenX;
        int screenY = worldY - gp.player.worldY + gp.player.screenY;

        // STOP MOVING CAMERA
        if (gp.player.worldX < gp.player.screenX) {
            screenX = worldX;
        }
        if (gp.player.worldY < gp.player.screenY) {
            screenY = worldY;
        }
        int rightOffset = gp.screenWidth - gp.player.screenX;
        if (rightOffset > gp.worldWidth - gp.player.worldX) {
            screenX = gp.screenWidth - (gp.worldWidth - worldX);
        }
        int bottomOffset = gp.screenHeight - gp.player.screenY;
        if (bottomOffset > gp.worldHeight - gp.player.worldY) {
            screenY = gp.screenHeight - (gp.worldHeight - worldY);
        }
        ///////////////////

        switch (direction) {
            case "up":
                if (spriteNum == 1) {
                    image = up0;
                }
                if (spriteNum == 2) {
                    image = up1;
                }
                break;
            case "down":
                if (spriteNum == 1) {
                    image = down0;
                }
                if (spriteNum == 2) {
                    image = down1;
                }
                break;
            case "left":
                if (spriteNum == 1) {
                    image = left0;
                }
                if (spriteNum == 2) {
                    image = left1;
                }
                break;
            case "right":
                if (spriteNum == 1) {
                    image = right0;
                }
                if (spriteNum == 2) {
                    image = right1;
                }
                break;
        }

        // Enemy HP bar
        if (type == 2 && hpBarOn) {

            double oneScale = (double) gp.tileSize / maxLife;
            double hpBarValue = oneScale * life;

            g2.setColor(new Color(35, 35, 35));
            g2.fillRect(screenX - 1, screenY - 16, gp.tileSize + 2, 12);

            g2.setColor(new Color(255, 0, 30));
            g2.fillRect(screenX, screenY - 15, (int) hpBarValue, 10);

            hpBarCounter++;

            if (hpBarCounter > 600) { // after 10 sec, the bar disappears
                hpBarCounter = 0;
                hpBarOn = false;
            }
        } // end if

        if (invincible) {
            hpBarOn = true;
            hpBarCounter = 0;
            changeAlpha(g2, 0.4f); // make enemy transparent when invincible, he received damage
        }

        if (dying) {
            dyingAnimation(g2);
        }

        if (worldX + gp.tileSize > gp.player.worldX - gp.player.screenX &&
                worldX - gp.tileSize < gp.player.worldX + gp.player.screenX &&
                worldY + gp.tileSize > gp.player.worldY - gp.player.screenY &&
                worldY - gp.tileSize < gp.player.worldY + gp.player.screenY) {
            g2.drawImage(image, screenX, screenY, null);
        }
        // If player is around the edge, draw everything
        else if (gp.player.worldX < gp.player.screenX ||
                gp.player.worldY < gp.player.screenY ||
                rightOffset > gp.worldWidth - gp.player.worldX ||
                bottomOffset > gp.worldHeight - gp.player.worldY) {
            g2.drawImage(image, screenX, screenY, null);
        }
        changeAlpha(g2, 1f);

        // DEBUG AND CHECK HITBOX
//        g2.setColor(new Color(255, 0, 30));
//        g2.fillRect(screenX, screenY, solidArea.width, solidArea.height);

    } // end draw

    /**
     * Animates the dying process of the Entity.
     *
     * @param g2 The Graphics2D object to draw on.
     */
    public void dyingAnimation(Graphics2D g2) {

        dyingCounter++;

        int i = 5;

        if (dyingCounter <= i) {
            changeAlpha(g2, 0f);
        }
        if (dyingCounter > i && dyingCounter <= i * 2) {
            changeAlpha(g2, 1f);
        }
        if (dyingCounter > i * 2 && dyingCounter <= i * 3) {
            changeAlpha(g2, 0f);
        }
        if (dyingCounter > i * 3 && dyingCounter <= i * 4) {
            changeAlpha(g2, 1f);
        }
        if (dyingCounter > i * 4 && dyingCounter <= i * 5) {
            changeAlpha(g2, 0f);
        }
        if (dyingCounter > i * 5 && dyingCounter <= i * 6) {
            changeAlpha(g2, 1f);
        }
        if (dyingCounter > i * 6 && dyingCounter <= i * 7) {
            changeAlpha(g2, 0f);
        }
        if (dyingCounter > i * 7 && dyingCounter <= i * 8) {
            changeAlpha(g2, 1f);
        }
        if (dyingCounter > i * 8) {
            alive = false;
        }

    } // end dyingAnimation

    /**
     * Changes the alpha (transparency) of the Entity.
     *
     * @param g2          The Graphics2D object to draw on.
     * @param alphaValue  The alpha value (transparency) to set.
     */
    public void changeAlpha(Graphics2D g2, float alphaValue) {

        g2.setComposite(AlphaComposite.getInstance(AlphaComposite.SRC_OVER, alphaValue));

    } // end changeAlpha

    /**
     * Sets up and scales an image based on the provided parameters.
     *
     * @param imagePath The path to the image resource.
     * @param width     The desired width of the image.
     * @param height    The desired height of the image.
     * @return A BufferedImage object representing the scaled image.
     */
    public BufferedImage setup(String imagePath, int width, int height) {

        UtilityTool uTool = new UtilityTool();
        BufferedImage image = null;

        try {
            image = ImageIO.read(getClass().getResourceAsStream(imagePath + ".png"));
            image = uTool.scaleImage(image, width, height);

        } catch (IOException e) {
            e.printStackTrace();
        }
        return image;
    } // end setup

} // end class
