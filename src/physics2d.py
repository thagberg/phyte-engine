from system import System
from events import *
from math import ceil

class PhysicsComponent(object):
    def __init__(self, entity_id, box=None, body=None):
        self.entity_id = entity_id
        self.box = box 
        self.collideables = list()
        self.body = body


class PhysicsSystem(System):
    def __init__(self, factory, components=None, active_components=None):
        super(PhysicsSystem, self).__init__()
        self.factory = factory
        self.components = list() if components is None else components
        self.active_components = list() if active_components is None else active_components

    def _add(self, component):
        self.components.append(component)

    def _remove(self, component):
        try:
            self.components.remove(component)
            self.components.append(component)
        except ValueError as e:
            print "Error when attempting to remove component from PhysicsManager: %s" % e.strerror

    def _add_active(self, component):
        self.active_components.append(component)

    def _remove_active(self, component):
        try:
            self.active_components.remove(component)
            self.components.remove(component)
        except ValueError as e:
            print "Error when attempting to remove component from PhysicsManager: %s" % e.strerror

    def handle_event(self, event):
        if event.type == ADDPHYSICSCOMPONENT:
            self._add(event.component)
        elif event.type == ADDPHYSICSCOMPONENTACTIVE:
            self._add_active(event.component)
        elif event.type == REMOVEPHYSICSCOMPONENT:
            self._remove(event.component)
        elif event.type == REMOVEPHYSICSCOMPONENTACTIVE:
            self._remove_active(event.component)
        elif event.type == COLLISION:
            self.handle_collision(event.box1, event.box2, event.mtv)

    def get_min_trans_vect(self, rect1, rect2):
        mtv = [0, 0]
        shift_left = (rect2[0] - (rect1[0] + rect1[2])) + 1
        shift_right = (rect1[0] - (rect2[0] + rect2[2])) + 1
        shift_up = (rect2[1] - (rect1[1] + rect1[3])) + 1
        shift_down = (rect[1] - (rect2[1] +rect2[3])) + 1

        mtv[0] = shift_left if shift_Left >= shift_right else shift_right
        mtv[1] = shift_up if shift_up >= shift_down else shift_down
        return mtv

    def handle_collision(box1, box2, mtv):
        if box1.hitactive:
            if not box1.expired:
                box1.expired = True 
                if box2.hurtactive:
                    hit_event = GameEvent(HIT_HURT,
                                          hitter=box1.entity_id,
                                          hittee=box2.entity_id,
                                          damage=box1.damage,
                                          stun=box1.stun,
                                          hitstun=box1.hitstun,
                                          push=box1.push)
                elif box2.blockactive:
                    hit_event = GameEvent(HIT_BLOCK,
                                          hitter=box1.entity_id,
                                          hittee=box2.entity_id,
                                          blockstun=box1.blockstun,
                                          push=box1.push)
                self.delegate(hit_event)
        elif box1.solid and box2.solid:
            create_comp = self.factory.create_component
            if box1.moveable:
                if box2.moveable:
                    # move each box half the mtv
                    split_mtv = [int(ceil(float(mtv[0])/2)), 
                                 int(ceil(float(mtv[1])/2))]
                    box2_mtv = [0-split_mtv[0], 0-split_mtv[1]]
                    create_comp('incmovement',
                                entity_id=box1.entity_id,
                                body=box1,
                                velocity=split_mtv)
                    create_comp('incmovement',
                                entity_id=box2.entity_id,
                                body=box2,
                                velocity=box2_mtv)
                else:
                    # move box1 the entire mtv
                    create_comp('incmovement',
                                entity_id=box1.entity_id,
                                body=box1,
                                velocity=mtv)
            elif box2.moveable:
                # move box2 the entire mtv
                box2_mtv = [0-mtv[0], 0-mtv[1]]
                create_comp('incmovement',
                            entity_id=box2.entity_id,
                            body=box2,
                            velocity=box2_mtv)

    def update(self, time, events=None):
        for comp in self.active_components:
            comp_rect = comp.box.rect

            # determine the list of collideable components
            box = comp.box
            if box.hitactive:
                coll_rects = [x.box.rect for x in self.components if
                                (x.box.blockactive or x.box.hurtactive) and 
                                not x.box.expired]
            elif box.solid:
                coll_rects = [x.box.rect for x in self.components if
                                x.box.solid]
            
            # find the indices of collisions
            collisions = comp_rect.collidelistall(coll_rects)
            # process each collision
            for coll_ind in collisions:
                coll_rect = coll_rects[coll_ind]
                mtv = self.get_min_trans_vect(comp_rect, coll_rect)
                c_event = GameEvent(COLLISION, box1=comp.box,
                                    box2=comp.collideables[coll_ind].box, 
                                    mtv=mtv)
                self.delegate(c_event)
