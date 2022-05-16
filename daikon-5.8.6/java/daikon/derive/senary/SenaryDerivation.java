package daikon.derive.senary;

import daikon.ValueTuple;
import daikon.VarInfo;
import daikon.derive.Derivation;
import daikon.derive.ValueAndModified;
import org.checkerframework.checker.lock.qual.GuardSatisfied;
import org.checkerframework.dataflow.qual.Pure;
import org.checkerframework.dataflow.qual.SideEffectFree;
import org.plumelib.util.ArraysPlume;

/** Abstract class to represent a derived variable that came from three base variables. */
public abstract class SenaryDerivation extends Derivation {
  // We are Serializable, so we specify a version to allow changes to
  // method signatures without breaking serialization.  If you add or
  // remove fields, you should change this number to the current date.
  static final long serialVersionUID = 20211016L;

  /** Original variable 1. */
  VarInfo base1;

  /** Original variable 2. */
  VarInfo base2;

  /** Original variable 3. */
  VarInfo base3;

  /** Original variable 4. */
  VarInfo base4;

  /** Original variable 5. */
  VarInfo base5;

  /** Original variable 6. */
  VarInfo base6;
  /**
   * Create a new TernaryDerivation from three varinfos.
   *
   * @param vi1 original variable 1
   * @param vi2 original variable 2
   * @param vi3 original variable 3
   * @param vi1 original variable 4
   * @param vi2 original variable 5
   * @param vi3 original variable 6
   */
  protected SenaryDerivation(VarInfo vi1, VarInfo vi2, VarInfo vi3, VarInfo  vi4, VarInfo vi5, VarInfo vi6) {
    base1 = vi1;
    base2 = vi2;
    base3 = vi3;
    base4 = vi4;
    base5 = vi5;
    base6 = vi6; 
  }

  @SideEffectFree
  @Override
  public SenaryDerivation clone(daikon.derive.senary.SenaryDerivation this) {
    try {
      return (SenaryDerivation) super.clone();
    } catch (CloneNotSupportedException e) {
      throw new Error("This can't happen", e);
    }
  }

  @SideEffectFree
  @Override
  public VarInfo[] getBases() {
    return new VarInfo[] {base1, base2, base3, base4, base5, base6};
  }

  @Pure
  @Override
  public VarInfo getBase(int i) {
    switch (i) {
      case 0:
        return base1;
      case 1:
        return base2;
      case 2:
        return base3;
      case 3:
        return base4;
      case 4:
        return base5;
      case 5:
        return base6;
      default:
        throw new Error("bad base: " + i);
    }
  }

  @Override
  public Derivation switchVars(VarInfo[] old_vars, VarInfo[] new_vars) {
    SenaryDerivation result = this.clone();
    result.base1 = new_vars[ArraysPlume.indexOf(old_vars, result.base1)];
    result.base2 = new_vars[ArraysPlume.indexOf(old_vars, result.base2)];
    result.base3 = new_vars[ArraysPlume.indexOf(old_vars, result.base3)];
    result.base4 = new_vars[ArraysPlume.indexOf(old_vars, result.base4)];
    result.base5 = new_vars[ArraysPlume.indexOf(old_vars, result.base5)];
    result.base6 = new_vars[ArraysPlume.indexOf(old_vars, result.base6)];
    return result;
  }

  @Override
  public abstract ValueAndModified computeValueAndModified(ValueTuple full_vt);

  @Pure
  @Override
  protected boolean isParam() {
    return (base1.isParam() || base2.isParam() || base3.isParam() || base4.isParam() || base5.isParam() || base6.isParam());
  }

  @Override
  public int derivedDepth() {
    return 1 + Math.max(base1.derivedDepth(), Math.max(base2.derivedDepth(), Math.max(base3.derivedDepth(), Math.max(base4.derivedDepth(), Math.max(base5.derivedDepth(), base6.derivedDepth())) )));
  }

  @Override
  public boolean canBeMissing() {
    return base1.canBeMissing || base2.canBeMissing || base3.canBeMissing || base4.canBeMissing || base5.canBeMissing || base6.canBeMissing;
  }

  @Pure
  @Override
  public boolean isDerivedFromNonCanonical() {
    // We insist that both are canonical, not just one.
    return !(base1.isCanonical() && base2.isCanonical() && base3.isCanonical() && base4.isCanonical() && base5.isCanonical() && base6.isCanonical());
  }
}
