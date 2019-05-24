import unittest
import tanki
import tkinter


class MyTest(unittest.TestCase):

    def test_collision_tank_treasure(self):

        TK_ROOT = tkinter.Tk()
        FIELD_ = tanki.FIELD()
        treasure_coords = FIELD_.TREASURE_BLOCK_COORDS[0]
        FIELD_.tanks[0].coords = treasure_coords
        self.assertEqual(FIELD_.tanks[0].tank_found_treasure(), 0)

    def test_collision_bullet_treasure(self):

        TK_ROOT = tkinter.Tk()
        FIELD_ = tanki.FIELD()
        FIELD_.tanks[0].tank_fire('<space>')
        FIELD_.update_bullets()
        self.assertEqual(FIELD_.remove_all_widjets_from_field(2), 0)

    def test_update_time(self):

        TK_ROOT = tkinter.Tk()
        FIELD_ = tanki.FIELD()
        FIELD_.time_init += 65
        FIELD_.update_play_time()
        self.assertEqual(FIELD_.remove_all_widjets_from_field(0), 0)

    def test_treasure_gen_block(self):

        TK_ROOT = tkinter.Tk()
        FIELD_ = tanki.FIELD()
        flag = False
        for _b in FIELD_.BLOCKS:
            if FIELD_.TREASURE_BLOCK_COORDS[0] == _b.coords:
                flag = True
        self.assertEqual(flag, True)

    def test_gen_block(self):

        TK_ROOT = tkinter.Tk()
        FIELD_ = tanki.FIELD()
        flag = False
        for _b in FIELD_.BLOCKS:
            if(_b.coords[1] > tanki.ROWS and
               _b.coords[0] > tanki.COLUMNS):
                flag = True
        self.assertEqual(flag, False)


if __name__ == '__main__':
    unittest.main()
