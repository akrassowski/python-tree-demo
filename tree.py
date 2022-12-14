#!/bin/env python
"""Publish shapes to form a Christmas Tree"""
import rti.connextdds as dds
import time
import argparse
SHAPE_TYPE = dds.QosProvider("tree.xml").type("tree_lib", "ShapeType")
HANDLE = dds.InstanceHandle.nil()

def draw_tree(writer):
    """Draw the large triangle and some detail branches"""
    instance = dds.DynamicData(SHAPE_TYPE)
    instance.set_string("color", "GREEN")
    instance.set_int("x", 128)
    instance.set_int("y", 120)
    instance.set_int("shapesize", 200)
    writer.write(instance, HANDLE)
    loc = [
        [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0],
        [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0],
        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        ]
    SIZE = 20
    instance.set_string("color", "GREEN")
    instance.set_int("shapesize", SIZE)
    DELTA_X, DELTA_Y = (SIZE * 0.50), SIZE
    START_X, START_Y = 122-((DELTA_X*0.5*len(loc[0]))), 38
    y = START_Y
    for row in loc:
        x = START_X
        for item in row:
            x += DELTA_X
            if item:
                instance.set_int("x", int(x))
                instance.set_int("y", int(y))
                writer.write(instance, HANDLE)
        y += DELTA_Y


def draw_trunk(writer):
    """Draw the trunk as a Square."""
    instance = dds.DynamicData(SHAPE_TYPE)
    instance.set_string("color", "BROWN")
    size = 40
    x, y = 128 , 235

    instance.set_int("shapesize", size)
    instance.set_int("x", x)
    instance.set_int("y", y)
    writer.write(instance, HANDLE)

def draw_balls(writer):
    """Draw some balls in red."""
    instance = dds.DynamicData(SHAPE_TYPE)
    size = 10
    start_x1 = 105
    start_x2 = start_x1-(size*4)
    start_x3 = start_x2 - (size * 3)
    pos = [
        [start_x1, 83],
        [size*1.5+start_x1, 83+size],
        [size*3+start_x1, 83],
        [size*4.5+start_x1, 83+size],

        [size*1.5+start_x2, 123+size],
        [size*3+start_x2, 123],
        [size*4.5+start_x2, 123+size],
        [size*6+start_x2, 123],
        [size*7.5+start_x2, 123+size],
        [size*9.0+start_x2, 123],
        [size*10.5+start_x2, 123+size],

        [size*1.5+start_x3, 173+size],
        [size*3+start_x3, 173],
        [size*4.5+start_x3, 173+size],
        [size*6+start_x3, 173],
        [size*7.5+start_x3, 173+size],
        [size*9.0+start_x3, 173],
        [size*10.5+start_x3, 173+size],
        [size*12.0+start_x3, 173],
        [size*13.5+start_x3, 173+size],
        [size*15.0+start_x3, 173],
        [size*16.5+start_x3, 173+size],
    ]
    instance.set_int("shapesize", size)
    instance.set_string("color", "RED")
    for x, y in pos:
        instance.set_int("x", int(x))
        instance.set_int("y", int(y))
        writer.write(instance, HANDLE)

def draw_topper(writer):
    """Draw the tree topper"""
    instance = dds.DynamicData(SHAPE_TYPE)
    instance.set_string("color", "YELLOW")
    size, x, y = 30, 128, 15
    instance.set_int("x", x)
    instance.set_int("y", y)
    instance.set_int("shapesize", size)
    writer.write(instance, HANDLE)

def publisher_main(domain_id):
    participant = dds.DomainParticipant(domain_id)
    writer_qos = dds.QosProvider.default.datawriter_qos
    topic = dds.DynamicData.Topic(participant, "Triangle", SHAPE_TYPE)
    tree_writer = dds.DynamicData.DataWriter(dds.Publisher(participant), topic, writer_qos)

    topic = dds.DynamicData.Topic(participant, "Square", SHAPE_TYPE)
    trunk_writer = dds.DynamicData.DataWriter(dds.Publisher(participant), topic, writer_qos)

    topic = dds.DynamicData.Topic(participant, "Circle", SHAPE_TYPE)
    ball_writer = dds.DynamicData.DataWriter(dds.Publisher(participant), topic, writer_qos)

    while 1:
        draw_trunk(trunk_writer)
        draw_tree(tree_writer)
        #draw_balls(ball_writer)
        draw_balls(ball_writer)
        for n in range(5):
            draw_balls(ball_writer)
            draw_topper(ball_writer)
            time.sleep(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="RTI Connext DDS Publish Tree"
    )
    parser.add_argument("-d", "--domain", type=int, default=0, help="DDS Domain ID")

    args = parser.parse_args()
    assert 0 <= args.domain < 233

    print("""
    This Python program will publish a set of shapes.
    Run the Shapes Demo and subscribe to Square.
    Also subscribe to Triangle and Circle with a depth of 100.
    When that's running, hit the Enter key to continue.""", flush=True)
    input()
    print("""Use Control-C to terminate.""", flush=True)
    publisher_main(args.domain)

