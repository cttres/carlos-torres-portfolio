/**
 * The GamePanel class serves as the core component for game rendering and logic control.
 * It provides the main canvas for rendering graphics, manages game parameters like tile size, screen dimensions, and frame rate,
 * and contains the game loop, which updates the game state and renders graphics. 
 */

package main;

import java.awt.Color;
import java.awt.Dimension;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Comparator;

import javax.swing.JPanel;

import entity.Player;
import entity.Entity;
import tile.TileManager;

@SuppressWarnings("serial")
public class GamePanel extends JPanel implements Runnable{

	// Changing these will affect player images, entity.setupPlayer(), menu image
	// Screen Settings
	final int originalTileSizeWidth = 15;   // 15x22 tile
	final int originalTileSizeHeight = 19;		// change to adapt to different screens, 22 to 19
	final int scale = 3;	// Scaling factor
	
	public final int tileSizeWidth = originalTileSizeWidth * scale;   // depends on scale
	public final int tileSizeHeight = originalTileSizeHeight * scale;
	public final int tileSize = tileSizeHeight;

	public final int maxScreenCol = 22;
	public final int maxScreenRow = 14;
	public final int screenWidth = tileSize * maxScreenCol;   // 912 pixels
	public final int screenHeight = tileSize * maxScreenRow;   // 720 pixels
	
	// WORLD SETTINGS
	public final int maxWorldCol = 50;
	public final int maxWorldRow = 50;
	public final int worldWidth = tileSize * maxWorldCol;
	public final int worldHeight = tileSize * maxWorldRow;
	
	
	// Frames per second
	int FPS = 60;

	//SYSTEM
	TileManager tileM = new TileManager(this);
	public KeyHandler keyH = new KeyHandler(this);
	Sound music = new Sound();
	Sound se = new Sound();
	public CollisionChecker cChecker = new CollisionChecker(this);
	public AssetSetter aSetter = new AssetSetter(this);
	public UI ui = new UI(this);
	public EventHandler eHandler = new EventHandler(this);
	Config config = new Config(this);
	Thread gameThread;
	
	// ENTITY AND OBJECT
	public Player player = new Player(this, keyH);
	
	// objects that can be displayed at the same time, it can be change any time to display more objects
	public Entity obj[] = new Entity[20];  //20 slots for objects
	public Entity enemy[] = new Entity[70];
	ArrayList<Entity> entityList = new ArrayList<>();
	public ArrayList<Entity> projectileList = new ArrayList<>();
	
	//GAME STATE
	public int gameState;
	public final int titleState = 0;
	public final int playState = 1;
	public final int pauseState = 2;
	public final int optionsState = 3;
	public final int gameOverState = 4;
	public final int endGameState = 5;
	
	
	public GamePanel() {
		
        // Set the preferred size of the game panel
		this.setPreferredSize(new Dimension(screenWidth, screenHeight));
		this.setBackground(Color.black);
		
		// all the drawing from this component will be done in an off-screen painting buffer
		// it can basically improve rendering performance
		this.setDoubleBuffered(true);   
		this.addKeyListener(keyH);
		this.setFocusable(true);	// With this, this GamePanel can be "focused" to receive key input
		
	}// end constructor

	
	// This places the objects into the map before the game loads
	public void setupGame() {
		
		aSetter.setObject();	// Place objects into the map
		aSetter.setEnemy();
		gameState = titleState; //changed
		playMusic(0);
	} //  end setupGame
	
	public void retry() {
		player.setDefaultPositions();
		player.restoreLife();
		aSetter.setEnemy();
		player.hasKey = 0;
	}
	public void restart() {
		player.setDefaultValues();
		aSetter.setEnemy();
		aSetter.setObject();
	}
	
	// clock that gives life to the game
	public void startGameThread() {
		gameThread = new Thread(this);
		gameThread.start();
	} // end startGameThread()
	
//	@Override
//	public void run() {
//		
//		double drawInterval = 1000000000/FPS; // 0.01666 seconds
//		double nextDrawTime = System.nanoTime() + drawInterval;		
//		
//		while (gameThread != null) {
//			
//						
//			// 1. Update: update information such as character positions
//			update();
//			
//			// 2. Draw: draw the screen with the updated information
//			repaint();
//			
//			
//			try {
//				double remainingTime = nextDrawTime - System.nanoTime();	
//				remainingTime = remainingTime/1000000;
//				
//				if (remainingTime < 0) {
//					remainingTime = 0;
//				}
//				
//				Thread.sleep( (long) remainingTime);
//				
//				nextDrawTime += drawInterval;
//				
//			} catch (InterruptedException e) {
//				e.printStackTrace();
//			}
//			
//		} // end while
//		
//	} // end run()
//
	
	public void run() {
		double drawInterval = 1000000000 / FPS;
		double delta = 0;
		long lastTime = System.nanoTime();		
		long currentTime;
		long timer = 0;
		int drawCount = 0;
		
		
		while (gameThread != null) {
			
			currentTime = System.nanoTime();
			
			delta += (currentTime - lastTime) / drawInterval;
			timer += (currentTime - lastTime);
			lastTime = currentTime;
			
			if (delta >= 1) {
				// 1. Update: update information such as character positions
				update();
				// 2. Draw: draw the screen with the updated information
				repaint();
				delta--;
				drawCount++;
			}
			
			if(timer >= 1000000000) {
				System.out.println("FPS: " + drawCount);
				drawCount = 0;
				timer = 0;
			}
			
		} // end while
	} // end run()
	
	
	// Update game elements
	public void update() {
		
		if(gameState == playState) {
			
			// PLAYER
			player.update();
			
			// ENEMY
			for (int i = 0; i < enemy.length; i++) {
				if(enemy[i] != null) {
					if(enemy[i].alive == true && enemy[i].dying == false) {
						enemy[i].update();
					}
					if(enemy[i].alive == false) {
						enemy[i].checkDrop();
						enemy[i] = null;
					}
				}
			} // end for
			
			// PROJECTILE
			for (int i = 0; i < projectileList.size(); i++) {
				if(projectileList.get(i) != null) {
					if(projectileList.get(i).alive == true) {
						projectileList.get(i).update();
					}
					if(projectileList.get(i).alive == false) {
						projectileList.remove(i);
					}
				}
			} // end for
			
		}// end if
		
		if(gameState == pauseState) {
			//nothing for now
		} // end if
		
	}// end update()
	
	
	// Paint component to render the game
	public void paintComponent(Graphics g) {
		
		super.paintComponent(g);
		
		Graphics2D g2 = (Graphics2D) g;
		
		//TITLE SCREEN
		if(gameState == titleState) {
			ui.draw(g2);
		} // end if
		
		//OTHERS
		else {
			//TILE
			tileM.draw(g2);
			
			// ADD ENTITIES TO THE LIST
			entityList.add(player);

			for(int i = 0; i < obj.length; i++) {
				if(obj[i] != null) {
					entityList.add(obj[i]);
				}
			} //  end for
			
			for(int i = 0; i < enemy.length; i++) {
				if(enemy[i] != null) {
					entityList.add(enemy[i]);
				}
			} //  end for
			
			for(int i = 0; i < projectileList.size(); i++) {
				if(projectileList.get(i) != null) {
					entityList.add(projectileList.get(i));
				}
			} //  end for
			
			// https://stackoverflow.com/questions/14154127/collections-sortlistt-comparator-super-t-method-example			
			// SORT
			Collections.sort(entityList, new Comparator<Entity>() {

				@Override
				public int compare(Entity e1, Entity e2) {
					int result = Integer.compare(e1.worldY, e2.worldY);
					return result;
				}
				
			});
			
			// DRAW ENTITIES
			for(int i = 0; i< entityList.size(); i++) {
				entityList.get(i).draw(g2);
			}// end for
			
			// EMPTY ENTITY LIST
			entityList.clear();

			
			//UI
			ui.draw(g2);
		} // end else
		

		
		g2.dispose();	// dispose of this graphics context and release any system resources that it is using
		
		
	}// paintComponent()
	
	
	// Method to play the music of the background
	public void playMusic(int i) {
		music.setFile(i);
		music.play();
		music.loop();
	} // end playMusic
	
	
	public void stopMusic() {
		music.stop();
	} // end stopMusic
	
	// This takes care of playing Sound Effects
	public void playSE(int i) {
		se.setFile(i); // 
		se.play();
	} // end playSE
	
	
	
	
} // end class

















