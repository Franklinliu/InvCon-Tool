package daikon.inv.unary.scalar;

import daikon.PptSlice;
import daikon.VarInfo;
import daikon.inv.DiscardInfo;
import daikon.inv.Invariant;
import daikon.inv.InvariantStatus;
import daikon.inv.OutputFormat;
import daikon.inv.ValueSet;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;
import org.checkerframework.checker.lock.qual.GuardSatisfied;
import org.checkerframework.checker.nullness.qual.Nullable;
import org.checkerframework.dataflow.qual.Pure;
import org.checkerframework.dataflow.qual.SideEffectFree;
import org.checkerframework.framework.qual.Unused;
import typequals.prototype.qual.Prototype;

import java.math.BigInteger;
/**
 * Tracks every unique value and how many times it occurs. Prints as {@code x has values: v1 v2 v3
 * ...}.
 */
public final class CompleteOneOfBigInt extends SingleBigInt {
  // We are Serializable, so we specify a version to allow changes to
  // method signatures without breaking serialization.  If you add or
  // remove fields, you should change this number to the current date.
  static final long serialVersionUID = 20220311L;

  /** Information about each value encountered. */
  public static class Info implements Serializable {
    static final long serialVersionUID = 20091210L;
    public BigInteger val;
    public int cnt;

    public Info(BigInteger val, int cnt) {
      this.val = val;
      this.cnt = cnt;
    }
  }

  /** List of values seen. */
  @Unused(when = Prototype.class)
  public List<Info> vals;

  /** Boolean. True iff CompleteOneOfScalar invariants should be considered. */
  public static boolean dkconfig_enabled = false;

  public CompleteOneOfBigInt(PptSlice slice) {
    super(slice);
    vals = new ArrayList<Info>();
  }

  public @Prototype CompleteOneOfBigInt() {
    super();
  }

  private static @Prototype CompleteOneOfBigInt proto = new @Prototype CompleteOneOfBigInt();

  /** Returns the prototype invariant for CompleteOneOFScalar. */
  public static @Prototype CompleteOneOfBigInt get_proto() {
    return proto;
  }

  /** returns whether or not this invariant is enabled */
  @Override
  public boolean enabled() {
    return dkconfig_enabled;
  }

  /** instantiate an invariant on the specified slice */
  @Override
  public CompleteOneOfBigInt instantiate_dyn(@Prototype CompleteOneOfBigInt this, PptSlice slice) {
    return new CompleteOneOfBigInt(slice);
  }

  /** Return description of invariant. Only Daikon format is implemented. */
  @SideEffectFree
  @Override
  public String format_using(@GuardSatisfied CompleteOneOfBigInt this, OutputFormat format) {
    if (format == OutputFormat.DAIKON) {
      String out = var().name() + " has values: ";
      for (Info val : vals) {
        out += String.format(" %s[%d]", val.val, val.cnt);
      }
      return out;
    } else {
      return format_unimplemented(format);
    }
  }

  /** Check to see if a only contains printable ascii characters. */
  @Override
  public InvariantStatus add_modified(BigInteger a, int count) {
    return check_modified(a, count);
  }

  /** Check to see if a only contains printable ascii characters. */
  @Override
  public InvariantStatus check_modified(BigInteger a, int count) {
    for (Info val : vals) {
      if (a.equals(val.val)) {
        val.cnt += count;
        return InvariantStatus.NO_CHANGE;
      }
    }
    vals.add(new Info(a, count));
    // System.out.printf("check_modified %s%n", format());
    return InvariantStatus.NO_CHANGE;
  }

  @Override
  protected double computeConfidence() {
    ValueSet vs = ppt.var_infos[0].get_value_set();
    // System.out.printf("%s value set = %s%n", ppt.var_infos[0].name(), vs);
    if (vs.size() > 0) {
      return Invariant.CONFIDENCE_JUSTIFIED;
    } else {
      return Invariant.CONFIDENCE_UNJUSTIFIED;
    }
  }

  /**
   * Returns whether or not this is obvious statically. The only check is for static constants which
   * are obviously printable (or not) from their values.
   */
  @Pure
  @Override
  public @Nullable DiscardInfo isObviousStatically(VarInfo[] vis) {
    return super.isObviousStatically(vis);
  }

  /**
   * Same formula if each value is the same and has the same count. Not implemented for now, just
   * presumed to be false.
   */
  @Pure
  @Override
  public boolean isSameFormula(Invariant o) {
    return false;
  }
}
