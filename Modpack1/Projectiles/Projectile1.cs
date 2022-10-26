using Terraria;
using Terraria.ID;
using Terraria.ModLoader;
using Microsoft.Xna.Framework;

namespace Modpack1.Projectiles
{
    public class Projectile1 : ModProjectile
    {
        public override void SetStaticDefaults()
        {
            DisplayName.SetDefault("Projectile1"); // By default, capitalization in classnames will add spaces to the display name. You can customize the display name here by uncommenting this line.
        }

        public override void SetDefaults()
        {
            Projectile.width = 13;
            Projectile.height = 13;
            Projectile.aiStyle = 0;
            Projectile.friendly = true;
            Projectile.hostile = false;
            Projectile.penetrate = 1;
            Projectile.timeLeft = 600;
            Projectile.light = 1f;
            Projectile.ignoreWater = true;
            Projectile.tileCollide = false;
        }


        public override void AI()
        {

            for (int i = 0; i < 200; i++)
            {
                NPC t = Main.npc[i];

                if (t.active && !t.friendly)
                {
                    // use vector2 instead of this
                    float dX = t.position.X + (float)t.width * 0.5f - Projectile.Center.X;
                    float dY = t.position.Y - Projectile.Center.Y;
                    float distance = (float)System.Math.Sqrt((double)(dX * dX + dY * dY));

                    if (distance < 480f)
                    {
                        distance = 3f / distance;
                        dX *= distance * 5;
                        dY *= distance * 5;

                        Projectile.velocity.X = dX;
                        Projectile.velocity.Y = dY;
                    }
                }
            }

            int dust = Dust.NewDust(Projectile.Center, 5, 5, 226, 0f, 0f, 0, default(Color), 1f);
            Main.dust[dust].velocity *= 0.3f;
            Main.dust[dust].scale = (float)Main.rand.Next(80, 115) * 0.013f;
            Main.dust[dust].noGravity = true;
        }
    }
}