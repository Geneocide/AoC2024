# import file data
# make map
# go through map, link adjacents together (E and S are next, W and N or prev)
# make regions of nodes like we did coords previously
# for each node check adjacents
# for each direction
# if adjacent is not the same crop then it's a side
# unless there is another, previous, orthogonal adjacent that has already counted that as a side
# another way to think of it might be go down the line, add 1 side to each region the first time you see that region
# and only remeber the last garden
# any gap would mean a corner which would mean a new side so only need to go back one to check
# store side count in region, not crop level, but any adjacent crop would be the same region so that helps
# do new price math Price = Area * Sides

# misc
# could store regions as a LL, it would make displaying them possible
# not sure it's efficient
# not sure it's necessary
